from redis.asyncio import Redis

async def get_redis():
    return Redis.from_url("redis://redis:6379")