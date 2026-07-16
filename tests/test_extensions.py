import pytest
from swarm_x.memory.store import InMemorySessionStore, JsonSessionStore, SessionRecord
from swarm_x.mcp import MCPToolAdapter
from swarm_x.skills import Skill, SkillRegistry

@pytest.mark.asyncio
async def test_memory_session_store():
    store = InMemorySessionStore()
    record = SessionRecord("abc", "task", [{"role": "user", "content": "hello"}])
    await store.save(record)
    assert (await store.load("abc")).task == "task"

@pytest.mark.asyncio
async def test_json_session_store(tmp_path):
    store = JsonSessionStore(tmp_path)
    await store.save(SessionRecord("abc", "task", []))
    assert (await store.load("abc")).session_id == "abc"

@pytest.mark.asyncio
async def test_mcp_adapter():
    class Client:
        async def call_tool(self, name, arguments): return {"name": name, "arguments": arguments}
    result = await MCPToolAdapter(Client(), "search").execute(query="hello")
    assert result["name"] == "search"

def test_skill_registry():
    skill = Skill("research", "Find reliable sources")
    registry = SkillRegistry([skill])
    assert registry.get("research").render().startswith("Skill: research")
