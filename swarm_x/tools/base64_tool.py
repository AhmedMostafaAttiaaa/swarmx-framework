import base64
from typing import Any
from .base import BaseTool

class Base64Tool(BaseTool):
    """Encodes/decodes base64 text, which LLMs frequently get subtly wrong by hand."""
    name = "base64"
    description = "Encodes or decodes text as base64. mode must be 'encode' or 'decode'."

    async def execute(self, text: str, mode: str = "encode", **kwargs: Any) -> str:
        if mode == "encode":
            return base64.b64encode(text.encode()).decode()
        if mode == "decode":
            return base64.b64decode(text.encode()).decode()
        raise ValueError("mode must be 'encode' or 'decode'")
