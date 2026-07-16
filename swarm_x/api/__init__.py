def create_app(engine):
    from dataclasses import asdict
    try: from fastapi import FastAPI
    except ImportError as e: raise RuntimeError("Install swarm-x[fastapi]") from e
    app=FastAPI(title="Swarm-X")
    @app.get("/health")
    async def health(): return {"status":"ok"}
    @app.get("/agents")
    async def agents(): return engine.registry.names()
    @app.post("/run")
    async def run(payload: dict): return asdict(await engine.run(payload["task"]))
    return app
