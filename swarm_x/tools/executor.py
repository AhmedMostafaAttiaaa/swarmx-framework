from typing import Any
from .base import BaseTool
class ToolExecutor:
    async def execute(self, tool: BaseTool, **kwargs: Any): return await tool.execute(**kwargs)

