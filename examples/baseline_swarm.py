"""Baseline Swarm-X team; choose Gemini or local Ollama with PROVIDER."""
import asyncio
import os
import sys
from swarm_x import BaseAgent, AgentOutput, SwarmEngine
from swarm_x.config import load_dotenv
from swarm_x.models import create_model

class BaselineAgent(BaseAgent):
    async def run(self, task, session, **kwargs):
        messages = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": task}]
        response = await self.model.generate(messages)
        return AgentOutput(response=response, context_updates={self.name: response})

async def main():
    load_dotenv()
    provider = os.getenv("PROVIDER", "ollama").lower()
    model_name = os.getenv("OLLAMA_MODEL" if provider == "ollama" else "GEMINI_MODEL", "llama3.2")
    model = create_model(provider, model_name)
    agents = [
        BaselineAgent("researcher", "Researches the task", "Give concise findings.", model),
        BaselineAgent("reviewer", "Reviews the answer", "Improve correctness and clarity.", model),
    ]
    task = " ".join(sys.argv[1:]).strip() or "Explain how this agent team works."
    result = await SwarmEngine(mode="workflow", workflow=agents).run(task)
    print(result.response)

if __name__ == "__main__": asyncio.run(main())
