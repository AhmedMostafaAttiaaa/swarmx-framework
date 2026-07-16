import os
from .settings import Settings
def load_yaml(path):
    try:
        import yaml
    except ImportError as e: raise RuntimeError("Install swarm-x[yaml] to load YAML") from e
    with open(path, encoding="utf-8") as f: data=yaml.safe_load(f) or {}
    def expand(v):
        if isinstance(v, str) and v.startswith("${") and v.endswith("}"): return os.getenv(v[2:-1], "")
        return v
    return Settings({k:{x:expand(y) for x,y in val.items()} for k,val in data.get("providers", {}).items()}, data.get("agents", {}))

