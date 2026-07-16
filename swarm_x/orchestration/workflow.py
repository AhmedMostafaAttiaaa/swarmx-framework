import asyncio
class WorkflowOrchestrator:
    async def run(self, engine, task, session):
        outputs=[]
        for agent in engine.workflow:
            outputs.append(await asyncio.wait_for(agent.run(task, session), engine.agent_timeout)); session.context.add(agent.name, outputs[-1].response)
        return outputs

