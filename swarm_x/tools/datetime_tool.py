from datetime import datetime, timezone
from typing import Any
from .base import BaseTool

class DateTimeTool(BaseTool):
    """Gives agents access to the current date/time, which they cannot infer on their own."""
    name = "datetime"
    description = "Returns the current UTC date and time, optionally formatted with strftime."

    async def execute(self, format: str | None = None, **kwargs: Any) -> str:
        now = datetime.now(timezone.utc)
        return now.strftime(format) if format else now.isoformat()
