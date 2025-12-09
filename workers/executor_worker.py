# workers/executor_worker.py
from workers.worker_base import WorkerBase

class ExecutorWorker(WorkerBase):
    ROLE = "Executor"

    async def execute(self, task):
        return {
            "role": "Executor",
            "action": f"Executing task: {task['input']}",
            "result": f"Done: {task['input']}"
        }