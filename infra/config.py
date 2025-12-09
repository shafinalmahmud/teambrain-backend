import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
INGRESS_STREAM = "tasks.ingress"
GROUP_NAME = "agent_workers"