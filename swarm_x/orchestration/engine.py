import asyncio
from ..agents.registry import AgentRegistry
from ..events.event_bus import EventBus
from ..events.event_types import Event
from ..memory.session import Session
from ..memory.store import SessionStore
from ..schemas.core import RunResult
from .swarm import SwarmOrchestrator
from .workflow import WorkflowOrchestrator
from .graph import GraphOrchestrator

class SwarmEngine:
    def __init__(self, mode="swarm", agents=None, workflow=None, graph=None, max_iterations=50, max_handoffs=50, agent_timeout=300, timeout=3600, loop_window=4, event_bus=None, session_store: SessionStore | None = None):
        if mode not in {"swarm", "workflow", "graph"}: raise ValueError("mode must be swarm, workflow, or graph")
        self.mode, self.registry, self.workflow, self.graph = mode, AgentRegistry(agents), list(workflow or []), graph or {}
        for agent in self.workflow: self.registry.register(agent)
        self.max_iterations, self.max_handoffs, self.agent_timeout, self.timeout, self.loop_window = max_iterations, max_handoffs, agent_timeout, timeout, loop_window
        self.events, self.event_bus = [], event_bus or EventBus()
        self.session_store = session_store
    async def emit(self, event): self.events.append(event); await self.event_bus.publish(event)
    async def run(self, task, state=None):
        session=Session(task, state, store=self.session_store); self.events=[]
        runner={"swarm": SwarmOrchestrator(), "workflow": WorkflowOrchestrator(), "graph": GraphOrchestrator()}[self.mode]
        outputs=await asyncio.wait_for(runner.run(self, task, session), self.timeout)
        await self.emit(Event("execution_finished", {"iterations": len(outputs)}))
        await session.persist()
        return RunResult(outputs[-1].response if outputs else None, outputs, self.events, len(outputs))
    async def stream(self, task, state=None):
        result=await self.run(task, state)
        for event in result.events: yield event
