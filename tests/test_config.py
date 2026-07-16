import os
from pathlib import Path
from swarm_x.config.env import load_dotenv
from swarm_x.models.gemini import GeminiLLM

def test_dotenv_loads_without_overwriting(monkeypatch):
    path = Path(__file__).with_name(".test.env")
    try:
        path.write_text("GEMINI_API_KEY=test-key\n# comment\n", encoding="utf-8")
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        assert load_dotenv(path)
        assert os.environ["GEMINI_API_KEY"] == "test-key"
    finally:
        path.unlink(missing_ok=True)

def test_gemini_requires_key(monkeypatch):
    monkeypatch.chdir(Path(__file__).parent)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    model = GeminiLLM()
    try:
        model._get_client()
    except RuntimeError as exc:
        assert "GEMINI_API_KEY" in str(exc)
    else:
        raise AssertionError("missing credentials should fail clearly")
