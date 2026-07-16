import pytest
from swarm_x import BaseAgent, AgentOutput, SwarmEngine
from swarm_x.memory.shared_state import SharedState
class Agent(BaseAgent):
    def __init__(self, name, nxt=None): super().__init__(name); self.nxt=nxt
    async def run(self, task, session, **kwargs): return AgentOutput(response=self.name, next_agent=self.nxt)
@pytest.mark.asyncio
async def test_workflow():
    r=await SwarmEngine("workflow", workflow=[Agent("a"),Agent("b")]).run("x")
    assert r.response == "b" and r.iterations == 2
@pytest.mark.asyncio
async def test_swarm_handoff():
    r=await SwarmEngine("swarm", agents=[Agent("a","b"),Agent("b")]).run("x")
    assert r.response == "b"
def test_state():
    s=SharedState(); s.set("x", 1); assert s.get("x")==1; s.update({"y":2}); s.delete("x"); assert s.get("x") is None
