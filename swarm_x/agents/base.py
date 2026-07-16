from abc import ABC, abstractmethod
from typing import Any
from .schemas import AgentOutput
from ..models.base import BaseLLM
from ..memory.session import Session

class BaseAgent(ABC):
    def __init__(self, name: str, description: str = "", system_prompt: str = "", model: BaseLLM | None = None, tools=None, metadata=None):
        self.name, self.description, self.system_prompt, self.model = name, description, system_prompt, model
        self.tools, self.metadata = list(tools or []), dict(metadata or {})
    @abstractmethod
    async def run(self, task: str, session: Session, **kwargs: Any) -> AgentOutput: ...

class LLMAnswerAgent(BaseAgent):
    async def run(self, task, session, **kwargs):
        if not self.model: return AgentOutput(response=task)
        messages = [{"role": "system", "content": self.system_prompt}, *session.context.messages(), {"role": "user", "content": task}]
        return AgentOutput(response=await self.model.generate(messages), context_updates={self.name: task})

