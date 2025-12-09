from fastapi import FastAPI
from orchestrator.router import router

app = FastAPI(title="TeamBrain Orchestrator")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "TeamBrain is alive. Send POST to /run"}