import json
from typing import Any
from .base import BaseTool

class JsonTool(BaseTool):
    """Validates and pretty-prints JSON, since LLMs often produce almost-valid JSON by hand."""
    name = "json_format"
    description = "Validates a JSON string and returns it pretty-printed with the given indent."

    async def execute(self, text: str, indent: int = 2, **kwargs: Any) -> str:
        return json.dumps(json.loads(text), indent=indent, sort_keys=False)
