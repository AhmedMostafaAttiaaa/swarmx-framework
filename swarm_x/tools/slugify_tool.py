import re
from typing import Any
from .base import BaseTool

class SlugifyTool(BaseTool):
    """Converts text into a URL/filename-safe slug."""
    name = "slugify"
    description = "Converts text into a lowercase, hyphen-separated slug."

    async def execute(self, text: str, **kwargs: Any) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return re.sub(r"-{2,}", "-", slug)
