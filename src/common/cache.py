import redis.asyncio as redis
import json

class RedisCache:
    def __init__(self, redis_url: str = "redis://redis:6379"):  # Utilisez "redis" comme hôte
        self.redis_url = redis_url
        self.redis = redis.Redis.from_url(self.redis_url)

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