from pydantic import BaseModel
from typing import Any, Dict

class ToolCall(BaseModel):
    tool: str
    args: Dict[str, Any]

class ToolResult(BaseModel):
    ok: bool
    result: Any