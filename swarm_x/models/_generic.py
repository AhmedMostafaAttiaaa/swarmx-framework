from .base import BaseLLM
class GenericLLM(BaseLLM):
    async def generate(self, messages, **kwargs):
        return messages[-1]["content"] if messages else ""

