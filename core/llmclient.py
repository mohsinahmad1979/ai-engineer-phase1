from abc import ABC, abstractmethod
from typing import Generator


class LLMClient(ABC):
    @abstractmethod
    def get_token_count(self, prompt: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def analyze_log_stream(
        self,
        log_content: str,
        retries: int = 3,
        initial_delay: int = 5,
    ) -> Generator[str, None, None]:
        raise NotImplementedError
