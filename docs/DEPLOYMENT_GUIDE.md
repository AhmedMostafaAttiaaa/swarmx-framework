# Deployment

Install optional FastAPI dependencies and expose `create_app(engine)`. Keep credentials in environment variables and provide application-specific model adapters through `BaseLLM`.

For local inference, install Ollama and pull a model, for example `ollama pull llama3.2`. Set `OLLAMA_HOST` and `OLLAMA_MODEL` in `.env`; no cloud credential is needed. Run `PROVIDER=ollama python examples/baseline_swarm.py` (PowerShell: `$env:PROVIDER="ollama"; python examples/baseline_swarm.py`).
