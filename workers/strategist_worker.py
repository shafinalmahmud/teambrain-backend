# workers/strategist_worker.py
from workers.worker_base import WorkerBase

class StrategistWorker(WorkerBase):
    ROLE = "Strategist"

    async def execute(self, task):
        return {
            "role": "Strategist",
            "plan": f"High-level strategy for: {task['input']}",
            "next_steps": ["Research needed", "Build execution plan"]
        }