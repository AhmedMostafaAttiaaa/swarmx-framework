import pytest
from swarm_x.mcp import InMemoryMCPClient, MCPToolAdapter
from swarm_x.skills import code_reviewer_skill, summarizer_skill

def test_summarizer_skill_renders():
    assert "summarizer" in summarizer_skill.render()

def test_code_reviewer_skill_renders():
    assert "code_reviewer" in code_reviewer_skill.render()

@pytest.mark.asyncio
async def test_in_memory_mcp_client_dispatches_registered_handler():
    client = InMemoryMCPClient()
    async def echo(text): return text
    client.register("echo", echo)
    result = await MCPToolAdapter(client, "echo").execute(text="hello")
    assert result == "hello"

@pytest.mark.asyncio
async def test_in_memory_mcp_client_unknown_tool_errors():
    client = InMemoryMCPClient()
    result = await MCPToolAdapter(client, "missing").execute()
    assert "error" in result
