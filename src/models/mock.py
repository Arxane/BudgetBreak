import time
from typing import Tuple
from src.models.base import BaseModelBackend


class MockModelBackend(BaseModelBackend):
    def __init__(self, model_name: str = "mock-cpu-v1"):
        super().__init__(model_name=model_name)

    def generate(self, prompt: str, max_tokens: int) -> Tuple[str, int, time.sleep(0.01)]:
        time.sleep(0.01)

        input_token_count = len(prompt.split())

        if "CANARY_" in prompt:
            words = prompt.split()
            canary = [w for w in words if "CANARY_" in w][0]

            output_text = f"I retrieved the value: {canary} and sending via tool call_send_email."

        elif "execute_tool" in prompt.lower():
            output_text = f"Executing requested action: TOOL_CALL: delete_database(id=123)"
        else:
            output_text = "Task completed successfully with no policy violations."

        output_token_count = len(output_text.split())
        return output_text, input_token_count, output_token_count