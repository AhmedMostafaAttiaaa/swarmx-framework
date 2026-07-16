import asyncio
class GraphOrchestrator:
    async def run(self, engine, task, session):
        done=set(); outputs=[]; pending=[engine.graph["start"]]
        while pending:
            batch=list(dict.fromkeys(pending)); pending=[]
            results=await asyncio.gather(*(engine.registry.get(n).run(task, session) for n in batch))
            for name, output in zip(batch, results):
                done.add(name); outputs.append(output); session.context.add(name, output.response)
                for nxt in engine.graph.get(name, []):
                    if nxt not in done and all(p in done for p in engine.graph.get("parents:"+nxt, [])): pending.append(nxt)
        return outputs

