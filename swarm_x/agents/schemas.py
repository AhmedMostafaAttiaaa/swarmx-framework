from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class AgentOutput:
    reasoning: str = ""
    response: Any = None
    next_agent: str | None = None
    tool_results: list[Any] = field(default_factory=list)
    context_updates: dict[str, Any] = field(default_factory=dict)
    shared_state_updates: dict[str, Any] = field(default_factory=dict)
    handoff_message: str = ""
    handoff_reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

