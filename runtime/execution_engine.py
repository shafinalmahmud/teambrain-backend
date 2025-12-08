# simplified worker loop (asyncio)
import asyncio, aioredis, json, uuid, time
from typing import Dict

LEASE_TTL = 30  # seconds
MAX_RETRIES = 5

async def claim_task(redis, stream='ingest', group='workers', consumer='w1'):
    # XREADGROUP to claim messages
    res = await redis.xread_group(group, consumer, streams={stream: '>'}, count=1, block=2000)
    return res  # raw message

async def process_message(msg):
    task = json.loads(msg['data'])
    task_id = task['task_id']
    step_index = task['current_stage']
    idempotency_key = f"{task_id}:{step_index}"
    if await check_idempotency(idempotency_key):
        return acknowledge(msg)
    try:
        # Acquire locks if needed
        # Fetch context bundle (cacheable)
        result = await execute_step(task)  # calls LLM, tools via tool_manager
        # validate via Guardian RPC
        await record_result(idempotency_key, result)
        # advance pipeline
        task['current_stage'] += 1
        await push_back_or_complete(task)
    except TransientError as e:
        await retry_with_backoff(msg)
    except PermanentError as e:
        await send_to_dead_letter(msg, reason=str(e))

async def worker_loop():
    redis = await aioredis.create_redis_pool("redis://localhost")
    while True:
        msg = await claim_task(redis)
        if not msg:
            await asyncio.sleep(0.1); continue
        await process_message(msg)