import hashlib
from typing import Any
from .base import BaseTool

_ALGORITHMS = {"md5", "sha1", "sha256", "sha512"}

class HashTool(BaseTool):
    """Lets agents compute checksums/digests of text without hallucinating them."""
    name = "hash"
    description = "Hashes text using md5, sha1, sha256, or sha512 (default sha256)."

    async def execute(self, text: str, algorithm: str = "sha256", **kwargs: Any) -> str:
        algorithm = algorithm.lower()
        if algorithm not in _ALGORITHMS:
            raise ValueError(f"Unsupported algorithm '{algorithm}'. Choose from: {sorted(_ALGORITHMS)}")
        return hashlib.new(algorithm, text.encode()).hexdigest()
