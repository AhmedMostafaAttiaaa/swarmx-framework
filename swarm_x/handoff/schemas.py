from dataclasses import dataclass, field
from typing import Any
@dataclass(slots=True)
class Handoff:
    source: str; target: str; message: str = ""; reason: str = ""; payload: dict[str, Any] = field(default_factory=dict); metadata: dict[str, Any] = field(default_factory=dict)

