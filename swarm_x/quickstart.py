"""Small application helpers for starting a Swarm-X project."""
import os
from typing import Any
from .agents.base import BaseAgent
from .agents.schemas import AgentOutput
from .config.env import load_dotenv
from .models import create_model
from .orchestration.engine import SwarmEngine

def model_from_env(provider: str | None = None):
    """Create Gemini or Ollama from the local .env configuration."""
    load_dotenv()
    selected = (provider or os.getenv("PROVIDER", "ollama")).lower()
    variable = "OLLAMA_MODEL" if selected == "ollama" else "GEMINI_MODEL"
    return create_model(selected, os.getenv(variable, "llama3.2" if selected == "ollama" else "gemini-2.5-flash"))

class PromptAgent(BaseAgent):
    """Simple reusable agent that sends the task to its injected model."""
    async def run(self, task: str, session, **kwargs: Any) -> AgentOutput:
        messages = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": task}]
        response = await self.model.generate(messages)
        return AgentOutput(response=response, context_updates={self.name: response})

def build_baseline_engine(provider: str | None = None) -> SwarmEngine:
    """Build a two-agent workflow using the configured provider."""
    model = model_from_env(provider)
    return SwarmEngine(mode="workflow", workflow=[
        PromptAgent("researcher", system_prompt="Answer with concise facts.", model=model),
        PromptAgent("reviewer", system_prompt="Review and improve the previous answer.", model=model),
    ])
