from contextlib import asynccontextmanager
class Tracer:
    def __init__(self): self.spans=[]
    @asynccontextmanager
    async def span(self, name, **attributes):
        span={"name":name, "attributes":attributes}; self.spans.append(span); yield span

