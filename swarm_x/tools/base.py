from abc import ABC, abstractmethod
from typing import Any
class BaseTool(ABC):
    name = "tool"; description = ""
    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any: ...

class CalculatorTool(BaseTool):
    name = "calculator"
    async def execute(self, expression: str, **kwargs): return eval(expression, {"__builtins__": {}}, {})

