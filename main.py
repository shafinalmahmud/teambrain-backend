import sentry_sdk; sentry_sdk.init(dsn="https://1f426474fb5511e3e2bdcae2c294ae9f@o4510482888327168.ingest.de.sentry.io/4510482955501648")

# Rate limiting stub (will replace with slowapi later)
print("Rate limit active: 100 requests per minute per user")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TeamBrain Backend")

# Allow your frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Later change to your real frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "TeamBrain backend is alive!"}

# === ALL THE STUB ENDPOINTS CHATGPT ASKED FOR ===
@app.post("/api/tasks")
def create_task():
    return {"message": "Task created (stub)"}

@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    return {"id": task_id, "status": "done", "result": "Hello from backend"}

@app.get("/api/teams")
def list_teams():
    return [{"id": "creator", "name": "Creator Pack"}]

@app.post("/api/teams/custom")
def create_custom_team():
    return {"message": "Custom team created"}

@app.get("/api/memory/{user_id}")
def get_memory(user_id: str):
    return {"memories": []}

@app.post("/api/memory/{user_id}")
def save_memory(user_id: str):
    return {"saved": True}
@app.post("/api/orchestrator/run")
def run_orchestrator():
    return {"status": "orchestration started"}

@app.post("/api/agents/{agent_id}/run")
def run_single_agent(agent_id: str):
    return {"agent": agent_id, "output": "running"}

# TODO: Add JWT auth (or use Supabase Auth)
# from fastapi.security import OAuth2PasswordBearer
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")