from typing import Any
from .base import BaseTool

class TextStatsTool(BaseTool):
    """Gives agents exact text metrics instead of estimating word/char counts by eye."""
    name = "text_stats"
    description = "Returns character, word, and line counts for the given text."

    async def execute(self, text: str, **kwargs: Any) -> dict[str, int]:
        return {
            "characters": len(text),
            "words": len(text.split()),
            "lines": len(text.splitlines()) or (1 if text else 0),
        }
