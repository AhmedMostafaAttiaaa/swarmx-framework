# Swarm-X

Swarm-X is a small, extensible Python framework for provider-agnostic multi-agent teams. Agent definitions are shared across three execution modes:

```python
from swarm_x import SwarmEngine
engine = SwarmEngine(mode="workflow", workflow=[researcher, writer, reviewer])
result = await engine.run("Research the topic")
```

## Architecture

Swarm-X separates agent behavior from model providers, tools, memory, and execution strategy. The same agents can run in swarm, workflow, or graph mode.

```text
Application / Streamlit / FastAPI / CLI
                  |
             SwarmEngine
       _________/ | \_________
      /           |           \
   Swarm       Workflow       Graph
      \           |           /
              BaseAgent
                  |
        AgentOutput + Handoff
          /        |        \
      Models     Tools      Events
        |          |           |
   Gemini       Serper      EventBus
   Ollama       MCP         Streaming
   OpenAI       Custom      Metrics/Tracing
   Groq
                  |
       Session + Context + SharedState
          |          |          |
    Chat history  LLM-visible  App-owned
                  memory       resources
```

### Core layers

- `agents/` defines reusable agents and the structured `AgentOutput` contract.
- `models/` provides provider adapters through the common `BaseLLM` interface.
- `orchestration/` executes agents using swarm routing, fixed workflows, or graph branches and joins.
- `memory/` separates model-visible context from application-owned shared state and optional session history.
- `tools/` contains injectable tools such as Serper search; `mcp/` adapts external MCP clients into tools.
- `events/`, `streaming/`, and `observability/` expose lifecycle events for UIs, logs, metrics, and tracing.
- `skills/` provides reusable instruction bundles without coupling them to a particular model.
- `config/` loads YAML and `.env` configuration while keeping secrets outside source control.

### Execution flow

1. The application creates an engine and registers agents.
2. The engine creates a session containing context and shared state.
3. The selected orchestrator runs agents with timeout and loop safeguards.
4. Agents return `AgentOutput`; they request handoffs by returning `next_agent`.
5. The engine resolves routing, publishes events, updates memory, and persists history when configured.
6. The application receives a `RunResult` or consumes the async event stream.

The core does not require an MCP server, Serper key, cloud model, database, or vector store. Those are optional application-level integrations.

Use `mode="swarm"` for agent-selected handoffs, `workflow` for fixed order, or `graph` for parallel DAG execution. Implement `BaseAgent.run()` and return `AgentOutput`; providers implement `BaseLLM`. Shared state is application-owned and never automatically sent to a model; `Context` is the model-visible memory.

Install the complete environment with `python -m pip install -r requirements.txt`. Run `swarmx validate` or `swarmx inspect` for basic CLI checks.

## Small Gemini test

After activating the Conda environment, run the included two-agent Gemini example:

```powershell
$env:PROVIDER = "gemini"
python examples/gemini_small_task.py
```

The reusable helpers in `swarm_x.quickstart` provide `model_from_env()` and `build_baseline_engine()` so applications do not need to repeat provider-selection code.

## Events and streaming

```powershell
python examples/stream_events.py
```

Applications can consume the same async event stream from a CLI, FastAPI endpoint, WebSocket, or UI adapter.

See the local [COMMANDS.md](COMMANDS.md) file for the complete command reference. It is intentionally ignored by Git so it remains a local operator cheat sheet.

## Tiny Streamlit UI

Install the UI extra and launch:

```powershell
python -m pip install -e ".[ui,gemini]"
streamlit run streamlit_app.py
```

Choose Gemini or Ollama, enter a task, and optionally enable Serper web search. Search results are added to the task context before it reaches the model, so a local Ollama model can use current web information without directly accessing the internet.

To enable search, add `SERPER_API_KEY` to `.env`. The tool uses Serper's JSON endpoint with the `X-API-KEY` header.

## Gemini configuration

Copy `.env.example` to `.env`, then set `GEMINI_API_KEY` to your private key:

```powershell
Copy-Item .env.example .env
notepad .env
pip install -e ".[gemini]"
```

Load it before constructing the model:

```python
from swarm_x.config import load_dotenv
from swarm_x.models import create_model
load_dotenv()
gemini = create_model("gemini", "gemini-2.5-flash")
```

`.env` is ignored by Git. Never commit the API key.

## Local Ollama

Install Ollama, pull a model, and set `OLLAMA_HOST`/`OLLAMA_MODEL` in `.env`. The baseline swarm defaults to Ollama:

```powershell
ollama pull llama3.2
python examples/baseline_swarm.py
```

To use Gemini instead:

```powershell
$env:PROVIDER = "gemini"
python examples/baseline_swarm.py
```

Give the swarm your repository task directly:

```powershell
python examples/baseline_swarm.py "Give me a Git repository name for this project and a short description."
```
