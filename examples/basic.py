import asyncio
from swarm_x import BaseAgent, AgentOutput, SwarmEngine
class Echo(BaseAgent):
    async def run(self, task, session, **kwargs): return AgentOutput(response=f"{self.name}: {task}")
async def main():
    result=await SwarmEngine(mode="workflow", workflow=[Echo("researcher"), Echo("reviewer")]).run("hello")
    print(result.response)
if __name__ == "__main__": asyncio.run(main())

