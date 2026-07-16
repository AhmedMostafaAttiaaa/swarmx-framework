from .base import BaseTool
class ToolRegistry:
    def __init__(self, tools=None): self._tools = {t.name: t for t in tools or []}
    def register(self, tool: BaseTool): self._tools[tool.name] = tool
    def get(self, name): return self._tools[name]
    def all(self): return list(self._tools.values())

