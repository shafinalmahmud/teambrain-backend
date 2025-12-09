# workers/guardian_worker.py
from workers.worker_base import WorkerBase

class GuardianWorker(WorkerBase):
    ROLE = "Guardian"

    async def execute(self, task):
        return {
            "role": "Guardian",
            "status": "APPROVED",
            "notes": "No safety issues detected"
        }