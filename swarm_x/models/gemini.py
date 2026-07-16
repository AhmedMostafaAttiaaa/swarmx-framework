import asyncio
import os
from collections.abc import AsyncIterator
from typing import Any
from .base import BaseLLM
from ..config.env import load_dotenv

class GeminiLLM(BaseLLM):
    """Gemini adapter using Google's current ``google-genai`` SDK."""
    def __init__(self, model: str = "gemini-2.5-flash", api_key: str | None = None, **config: Any):
        super().__init__(model, **config)
        load_dotenv()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self._client = None

    def _get_client(self):
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured. Put it in .env or the environment.")
        if self._client is None:
            try:
                from google import genai
            except ImportError as exc:
                raise RuntimeError("Install the Gemini extra: pip install -e '.[gemini]'") from exc
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    @staticmethod
    def _contents(messages: list[dict[str, str]]) -> str:
        return "\n\n".join(f"{m.get('role', 'user').title()}: {m.get('content', '')}" for m in messages)

    async def generate(self, messages, **kwargs):
        client = self._get_client()
        response = await asyncio.to_thread(client.models.generate_content, model=self.model, contents=self._contents(messages), config=kwargs or None)
        return getattr(response, "text", "") or ""

    async def stream(self, messages, **kwargs) -> AsyncIterator[str]:
        client = self._get_client()
        chunks = await asyncio.to_thread(lambda: list(client.models.generate_content_stream(model=self.model, contents=self._contents(messages), config=kwargs or None)))
        for chunk in chunks:
            text = getattr(chunk, "text", None)
            if text:
                yield text
