# Creating agents

Subclass `BaseAgent`, accept a `Session`, and return `AgentOutput`. Set `next_agent` to request a handoff; agents never invoke one another directly.

