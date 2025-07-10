import aioredis
import json

class RedisCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)

    async def get(self, key: str):
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: dict, expire: int = 60):
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def invalidate(self, key: str):
        await self.redis.delete(key)

cache = RedisCache()