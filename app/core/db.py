from typing import AsyncIterator
from redis.asyncio import from_url, Redis
from app.core.config import settings


async def init_redis_pool() -> AsyncIterator[Redis]:
    session = from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    try:
        yield session
    finally:
        await session.close()
