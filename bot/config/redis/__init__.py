import os
import redis.asyncio as redis


CACHE_TTL = 300
NEG_TTL = 30
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(REDIS_URL, decode_responses=True)
