from typing import Any, Protocol
from ..tools.base import BaseTool

class MCPClient(Protocol):
    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any: ...

class MCPToolAdapter(BaseTool):
    def __init__(self, client: MCPClient, name: str, description: str = ""):
        self.client = client
        self.name = name
        self.description = description or f"Executes the {name} tool via MCP client."
        
    async def execute(self, **kwargs): 
        try:
            return await self.client.call_tool(self.name, kwargs)
        except Exception as e:
            return {"error": f"Failed to execute MCP tool '{self.name}': {str(e)}"}