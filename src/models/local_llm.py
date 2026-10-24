import time
from typing import Tuple

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from src.models.base import BaseModelBackend


class LocalHFBackend(BaseModelBackend):
    def __init__(self, model_name: str = "mock-cpu-v1", load_in_4bit: bool = True):
        super().__init__(model_name=model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, trust_remote_code=True
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        if load_in_4bit and self.device == "cuda":
            quantization_config = BitsAndBytesConfig(
                load_in_4bits=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=quantization_config,
                device_map="auto",
                trust_remote_code=True,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto",
                trust_remote_code=True,
            )

    def generate(self, prompt: str, max_tokens: int) -> Tuple[str, int, int]:
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(self.device)
        input_token_count = inputs["input_ids"].shape[1]

        with torch.no_grad():
            output_ids = self.model.generate(**inputs, max_new_tokens=max_tokens, do_sample=False, pad_token_id=self.tokenizer.pad_token_id)


        generated_ids = output_ids[0][input_token_count:]
        output_token_count = len(generated_ids)

        output_text = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        return output_text, input_token_count, output_token_count