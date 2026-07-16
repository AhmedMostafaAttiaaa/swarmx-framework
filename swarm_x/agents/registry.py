from .base import BaseAgent
class AgentRegistry:
    def __init__(self, agents=None): self._agents = {a.name: a for a in agents or []}
    def register(self, agent: BaseAgent): self._agents[agent.name] = agent
    def get(self, name: str) -> BaseAgent: return self._agents[name]
    def all(self): return list(self._agents.values())
    def names(self): return list(self._agents)

