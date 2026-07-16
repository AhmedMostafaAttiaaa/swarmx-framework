import inspect
from collections import defaultdict
class EventBus:
    def __init__(self): self._subs = defaultdict(list)
    def subscribe(self, event_type, callback): self._subs[event_type].append(callback); return callback
    async def publish(self, event):
        for callback in [*self._subs.get(event.type, []), *self._subs.get("*", [])]:
            value = callback(event)
            if inspect.isawaitable(value): await value

