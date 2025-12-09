# orchestrator/router.py
from fastapi import APIRouter
from pydantic import BaseModel
from orchestrator.task_router import push_task

router = APIRouter()

class UserRequest(BaseModel):
    input: str
    metadata: dict = {}

@router.post("/run")
async def run_task(request: UserRequest):
    task_id = await push_task(request)
    return {"task_id": task_id, "status": "queued"}