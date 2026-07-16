class EventStream:
    def __init__(self): self._queue = None
    async def __aiter__(self):
        while self._queue:
            item = await self._queue.get()
            if item is None: break
            yield item

