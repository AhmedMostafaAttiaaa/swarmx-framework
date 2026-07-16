from uuid import uuid4
from .context import Context
from .shared_state import SharedState
from .store import SessionStore, SessionRecord
class Session:
    def __init__(self, task: str, state=None, session_id=None, store: SessionStore | None = None):
        self.session_id, self.context, self.state, self.store = session_id or uuid4().hex, Context(task), state or SharedState(), store
    async def persist(self):
        if self.store: await self.store.save(SessionRecord(self.session_id, self.context.task, self.context.items))
