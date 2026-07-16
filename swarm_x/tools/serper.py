import asyncio
import json
import os
from typing import Any
from urllib.request import Request, urlopen
from .base import BaseTool

class SerperSearchTool(BaseTool):
    """Optional Google search tool for agents using any model provider."""
    name = "web_search"
    description = "Search the web and return titles, links, and snippets."

    def __init__(self, api_key: str | None = None, endpoint: str = "https://google.serper.dev/search"):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        self.endpoint = endpoint

    async def execute(self, query: str, num_results: int = 5, **kwargs: Any) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("SERPER_API_KEY is not configured. Add it to .env to enable web search.")
        payload = json.dumps({"q": query, "num": num_results}).encode()
        request = Request(self.endpoint, data=payload, headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"})
        def call():
            with urlopen(request, timeout=kwargs.get("timeout", 30)) as response:
                return json.loads(response.read().decode())
        return await asyncio.to_thread(call)

    async def search_text(self, query: str, num_results: int = 5) -> str:
        data = await self.execute(query, num_results)
        results = data.get("organic", [])
        return "\n".join(f"- {item.get('title', '')}: {item.get('snippet', '')} ({item.get('link', '')})" for item in results)
