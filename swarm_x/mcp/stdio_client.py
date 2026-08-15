import asyncio
import itertools
import json
from typing import Any

class StdioMCPClient:
    """Minimal JSON-RPC 2.0 client for an MCP server spawned as a subprocess over stdio.

    Only implements the request/response calls needed to satisfy the MCPClient
    protocol (`call_tool`); notifications and server-initiated requests are not handled.
    """

    def __init__(self, command: str, args: list[str] | None = None):
        self.command = command
        self.args = args or []
        self._process: asyncio.subprocess.Process | None = None
        self._id_counter = itertools.count(1)

    async def start(self) -> None:
        self._process = await asyncio.create_subprocess_exec(
            self.command, *self.args,
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
        )

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        if self._process is None:
            await self.start()
        request = {
            "jsonrpc": "2.0",
            "id": next(self._id_counter),
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        }
        assert self._process.stdin and self._process.stdout
        self._process.stdin.write((json.dumps(request) + "\n").encode())
        await self._process.stdin.drain()
        line = await self._process.stdout.readline()
        response = json.loads(line.decode())
        if "error" in response:
            raise RuntimeError(response["error"])
        return response.get("result")

    async def close(self) -> None:
        if self._process is not None:
            self._process.stdin.close()
            await self._process.wait()
            self._process = None
