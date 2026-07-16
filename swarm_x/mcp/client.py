"""Optional MCP integration boundary.

The core does not depend on an MCP SDK. Applications can wrap an installed MCP
client with this protocol and expose discovered tools through the normal tool API.
"""
from typing import Any, Protocol
from ..tools.base import BaseTool

class MCPClient(Protocol):
    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any: ...

class MCPToolAdapter(BaseTool):
    def __init__(self, client: MCPClient, name: str, description: str = ""):
        self.client, self.name, self.description = client, name, description
    async def execute(self, **kwargs): return await self.client.call_tool(self.name, kwargs)
