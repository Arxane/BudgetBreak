from abc import ABC, abstractmethod
from typing import Tuple

class BaseModelBackend(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int) -> Tuple[str, int, int]:
        pass