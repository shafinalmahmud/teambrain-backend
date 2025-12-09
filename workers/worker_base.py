# workers/worker_base.py
import json
import asyncio
from infra.redis_client import get_redis
from infra.config import INGRESS_STREAM, GROUP_NAME
from infra.idempotency import is_done, mark_done

class WorkerBase:
    ROLE = None  # Must be set in child class

    async def run(self):
        redis = await get_redis()
        # Create consumer group if not exists
        try:
            await redis.xgroup_create(INGRESS_STREAM, GROUP_NAME, mkstream=True)
        except:
            pass  # Group already exists

        print(f"[{self.ROLE}] Worker started — waiting for tasks...")

        while True:
            msgs = await redis.xread_group(
                GROUP_NAME,
                self.ROLE,
                streams={INGRESS_STREAM: '>'},
                count=1,
                block=5000
            )

            

            if not msgs:
                continue

            stream, entries = msgs[0]
            msg_id, data = entries[0]
            payload = json.loads(data[b"data"].decode())

            await self.handle_task(redis, msg_id, payload)

    async def handle_task(self, redis, msg_id, task):
        # Skip if not this agent's turn
        if task["pipeline"][task["stage"]] != self.ROLE:
            await redis.xack(INGRESS_STREAM, GROUP_NAME, msg_id)
            return

        step_id = f"{task['task_id']}:{task['stage']}"

        # Idempotency check
        if is_done(step_id):
            print(f"[{self.ROLE}] Already processed {step_id}")
            await self.advance_task(redis, msg_id, task)
            return

        print(f"[{self.ROLE}] Processing: {task['input']}")

        result = await self.execute(task)

        mark_done(step_id, result)

        await self.advance_task(redis, msg_id, task)

    async def advance_task(self, redis, msg_id, task):
        task["stage"] += 1
        if task["stage"] >= len(task["pipeline"]):
            print(f"[{self.ROLE}] Task {task['task_id']} COMPLETED")
            await redis.xack(INGRESS_STREAM, GROUP_NAME, msg_id)
            return

        await redis.xadd(INGRESS_STREAM, {"data": json.dumps(task)})
        await redis.xack(INGRESS_STREAM, GROUP_NAME, msg_id)

    async def execute(self, task):
        """Override in child class"""
        raise NotImplementedError