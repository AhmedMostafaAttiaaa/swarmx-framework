from dataclasses import dataclass, field
from typing import Any
@dataclass(slots=True)
class Skill:
    name: str
    instructions: str
    tools: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    def render(self) -> str: return f"Skill: {self.name}\n{self.instructions}"
