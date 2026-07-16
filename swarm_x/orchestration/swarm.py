import asyncio
from ..events.event_types import Event
class SwarmOrchestrator:
    async def run(self, engine, task, session):
        name = engine.registry.names()[0] if engine.registry.names() else None; outputs=[]; visited=[]; handoffs=0
        while name:
            if len(outputs) >= engine.max_iterations or handoffs >= engine.max_handoffs: break
            if name in visited[-engine.loop_window:]: raise RuntimeError("Agent loop detected")
            visited.append(name); agent=engine.registry.get(name)
            await engine.emit(Event("agent_started", {"agent": name}))
            try: output=await asyncio.wait_for(agent.run(task, session), engine.agent_timeout)
            except Exception as exc: await engine.emit(Event("error", {"agent": name, "error": str(exc)})); raise
            outputs.append(output); session.context.add(name, output.response); session.context.update(output.context_updates); session.state.update(output.shared_state_updates)
            nxt=output.next_agent
            if nxt: handoffs += 1; await engine.emit(Event("handoff", {"source": name, "target": nxt}))
            await engine.emit(Event("agent_finished", {"agent": name})); name=nxt
        return outputs

