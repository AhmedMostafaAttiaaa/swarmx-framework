"""Pluggable conversation history stores."""
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

@dataclass(slots=True)
class SessionRecord:
    session_id: str
    task: str
    messages: list[dict[str, Any]]

class SessionStore(ABC):
    @abstractmethod
    async def load(self, session_id: str) -> SessionRecord | None: ...
    @abstractmethod
    async def save(self, record: SessionRecord) -> None: ...

class InMemorySessionStore(SessionStore):
    def __init__(self): self.records: dict[str, SessionRecord] = {}
    async def load(self, session_id): return self.records.get(session_id)
    async def save(self, record): self.records[record.session_id] = record

class JsonSessionStore(SessionStore):
    def __init__(self, directory: str | Path = ".swarm_x/sessions"):
        self.directory = Path(directory); self.directory.mkdir(parents=True, exist_ok=True)
    def _path(self, session_id): return self.directory / f"{session_id}.json"
    async def load(self, session_id):
        path = self._path(session_id)
        if not path.exists(): return None
        return SessionRecord(**json.loads(path.read_text(encoding="utf-8")))
    async def save(self, record):
        self._path(record.session_id).write_text(json.dumps(asdict(record), default=str, indent=2), encoding="utf-8")
