import asyncio
import json
import os
from collections.abc import AsyncIterator
from typing import Any
from urllib.request import Request, urlopen
from .base import BaseLLM

class OllamaLLM(BaseLLM):
    """Local Ollama adapter using its HTTP API; no Ollama SDK required."""
    def __init__(self, model: str = "llama3.2", host: str | None = None, **config: Any):
        super().__init__(model, **config)
        self.host = (host or os.getenv("OLLAMA_HOST", "http://localhost:11434")).rstrip("/")

    @staticmethod
    def _payload(model, messages, stream=False, **kwargs):
        return json.dumps({"model": model, "messages": messages, "stream": stream, **kwargs}).encode()

    def _request(self, messages, stream=False, **kwargs):
        request = Request(self.host + "/api/chat", data=self._payload(self.model, messages, stream, **kwargs), headers={"Content-Type": "application/json"})
        return urlopen(request, timeout=self.config.get("timeout", 300))

    async def generate(self, messages, **kwargs):
        def call():
            with self._request(messages, False, **kwargs) as response:
                data = json.loads(response.read().decode())
                return data.get("message", {}).get("content", "")
        return await asyncio.to_thread(call)

    async def stream(self, messages, **kwargs) -> AsyncIterator[str]:
        def open_stream(): return self._request(messages, True, **kwargs)
        response = await asyncio.to_thread(open_stream)
        try:
            while True:
                line = await asyncio.to_thread(response.readline)
                if not line: break
                data = json.loads(line.decode())
                text = data.get("message", {}).get("content", "")
                if text: yield text
        finally:
            response.close()
