import asyncio

async def echo(text: str):
    await asyncio.sleep(0.1)
    return f"ECHO: {text}"

TOOLS = {
    "echo": echo
}