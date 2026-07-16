"""Fail CI if common credential patterns are committed."""
from pathlib import Path
import re
import sys

PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"(?:GEMINI|GOOGLE|SERPER)_API_KEY\s*=\s*(?!your_|replace_|test-|fake|dummy)[^\s#]+", re.I),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
SKIP = {".env", ".git", ".pytest_cache", "__pycache__", ".pyc", "COMMANDS.md"}

def main() -> int:
    findings = []
    for path in Path(".").rglob("*"):
        if not path.is_file() or any(part in SKIP for part in path.parts): continue
        try: text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError): continue
        for pattern in PATTERNS:
            if pattern.search(text): findings.append(str(path)); break
    if findings:
        print("Potential secrets found:")
        print("\n".join(sorted(set(findings))))
        return 1
    print("Secret scan passed")
    return 0

if __name__ == "__main__": sys.exit(main())
