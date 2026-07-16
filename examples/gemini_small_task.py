"""Minimal Gemini API test for Swarm-X."""
import asyncio
from swarm_x.quickstart import build_baseline_engine

async def main():
    engine = build_baseline_engine("gemini")
    result = await engine.run("What is 2 + 2? Answer with only the number.")
    print(result.response)

if __name__ == "__main__": asyncio.run(main())
