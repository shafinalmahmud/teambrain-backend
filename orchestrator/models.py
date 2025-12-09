# orchestrator/models.py
from pydantic import BaseModel
from typing import Dict, Any

class UserRequest(BaseModel):
    input: str
    metadata: Dict[str, Any] = {}