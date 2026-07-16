from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class RunRequest:
    task: str
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class RunResult:
    response: Any = None
    outputs: list[Any] = field(default_factory=list)
    events: list[Any] = field(default_factory=list)
    iterations: int = 0

