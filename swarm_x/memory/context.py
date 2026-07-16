from typing import Any
class Context:
    def __init__(self, task: str, max_items: int = 50): self.task, self.max_items, self.items = task, max_items, []
    def add(self, role: str, content: Any, **metadata: Any) -> None:
        self.items.append({"role": role, "content": content, "metadata": metadata}); self.compress()
    def update(self, values: dict[str, Any]) -> None:
        for key, value in values.items(): self.add("context", {key: value})
    def compress(self) -> None:
        if len(self.items) > self.max_items: self.items = self.items[-self.max_items:]
    def messages(self) -> list[dict[str, str]]:
        return [{"role": "system", "content": f"Task: {self.task}"}] + [{"role": x["role"], "content": str(x["content"])} for x in self.items]

