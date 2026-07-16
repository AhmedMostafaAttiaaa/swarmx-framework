from typing import Any
class SharedState:
    def __init__(self, initial: dict[str, Any] | None = None): self._data = dict(initial or {})
    def set(self, key: str, value: Any) -> None: self._data[key] = value
    def get(self, key: str, default: Any = None) -> Any: return self._data.get(key, default)
    def update(self, values: dict[str, Any]) -> None: self._data.update(values)
    def delete(self, key: str) -> None: self._data.pop(key, None)
    def snapshot(self) -> dict[str, Any]: return dict(self._data)

