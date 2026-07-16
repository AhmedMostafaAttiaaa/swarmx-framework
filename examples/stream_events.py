"""Print orchestration events while running a configured provider."""
import asyncio
from swarm_x.quickstart import build_baseline_engine

async def main():
    engine = build_baseline_engine()
    async for event in engine.stream("Say hello in one short sentence."):
        print(f"[{event.type}] {event.data}")

if __name__ == "__main__": asyncio.run(main())
