import ast
import operator
from abc import ABC, abstractmethod
from typing import Any
class BaseTool(ABC):
    name = "tool"; description = ""
    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any: ...

_CALC_OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
    ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos,
}

def _eval_calc_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _CALC_OPERATORS:
        return _CALC_OPERATORS[type(node.op)](_eval_calc_node(node.left), _eval_calc_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _CALC_OPERATORS:
        return _CALC_OPERATORS[type(node.op)](_eval_calc_node(node.operand))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

class CalculatorTool(BaseTool):
    """Evaluates arithmetic via a restricted AST walk instead of eval(), so expressions
    can't reach builtins, attributes, or calls."""
    name = "calculator"
    async def execute(self, expression: str, **kwargs):
        return _eval_calc_node(ast.parse(expression, mode="eval").body)

