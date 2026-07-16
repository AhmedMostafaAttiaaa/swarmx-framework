from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
@dataclass(slots=True)
class Event:
    type: str; data: dict[str, Any] = field(default_factory=dict); timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

