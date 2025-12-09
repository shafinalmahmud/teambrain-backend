import uuid
import json
from infra.redis_client import get_redis
from infra.config import INGRESS_STREAM

async def push_task(request):
    redis = await get_redis()
    task_id = str(uuid.uuid4())

    task_payload = {
        "task_id": task_id,
        "pipeline": ["Strategist", "Executor", "Guardian"],
        "stage": 0,
        "input": request.input,
        "metadata": request.metadata or {}
    }

    await redis.xadd(INGRESS_STREAM, {"data": json.dumps(task_payload)})
    return task_id