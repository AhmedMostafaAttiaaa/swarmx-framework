# Architecture

The engine coordinates agents, memory, tools, events, and handoffs through small interfaces. Models and tools are dependency-injected. The orchestration layer knows only `BaseAgent` and `AgentOutput`, so provider and application concerns remain outside it.

