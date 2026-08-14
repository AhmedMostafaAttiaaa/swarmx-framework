import uuid
from typing import Any
from .base import BaseTool

class UUIDTool(BaseTool):
    """Generates unique identifiers for agents that need to tag sessions, traces, or artifacts."""
    name = "uuid"
    description = "Generates a random UUID4 string."

    async def execute(self, **kwargs: Any) -> str:
        return str(uuid.uuid4())
