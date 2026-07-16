from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

class BaseLLM(ABC):
    def __init__(self, model: str, **config: Any): self.model, self.config = model, config
    @abstractmethod
    async def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> Any: ...
    async def stream(self, messages: list[dict[str, str]], **kwargs: Any) -> AsyncIterator[str]:
        result = await self.generate(messages, **kwargs); yield str(result)
    async def count_tokens(self, messages: list[dict[str, str]]) -> int:
        return sum(len(m.get("content", "").split()) for m in messages)

