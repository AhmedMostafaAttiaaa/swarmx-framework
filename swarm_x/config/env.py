"""Minimal .env loader; avoids making dotenv a core dependency."""
from pathlib import Path
import os

def load_dotenv(path: str | Path = ".env", override: bool = False) -> bool:
    file = Path(path)
    if not file.exists():
        return False
    for raw in file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip("\"'")
        if override or key not in os.environ:
            os.environ[key] = value
    return True

