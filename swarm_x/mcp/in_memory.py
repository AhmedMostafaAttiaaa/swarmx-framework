from typing import Any, Awaitable, Callable

class InMemoryMCPClient:
    """A local MCPClient implementation backed by plain Python callables.

    Useful for tests and examples that need an MCPToolAdapter without
    standing up a real MCP server.
    """

    def __init__(self, handlers: dict[str, Callable[..., Awaitable[Any]]] | None = None):
        self._handlers = dict(handlers or {})

    def register(self, name: str, handler: Callable[..., Awaitable[Any]]) -> None:
        self._handlers[name] = handler

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        if name not in self._handlers:
            raise KeyError(f"No handler registered for MCP tool '{name}'")
        return await self._handlers[name](**arguments)
