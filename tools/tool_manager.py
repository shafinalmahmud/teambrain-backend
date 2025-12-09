from tools.schemas import ToolCall, ToolResult
from tools.builtin_tools import TOOLS

async def invoke_tool(tool_call: ToolCall):
    if tool_call.tool not in TOOLS:
        return ToolResult(ok=False, result="Unknown tool")

    try:
        result = await TOOLS[tool_call.tool](**tool_call.args)
        return ToolResult(ok=True, result=result)
    except Exception as e:
        return ToolResult(ok=False, result=str(e))