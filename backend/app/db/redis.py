
import logging

import redis.asyncio as redis
from redis.exceptions import ConnectionError as RedisConnectionError

from app.config import settings

logger = logging.getLogger(__name__)

redis_client = None


async def connect_to_redis():

    global redis_client

    redis_client = redis.Redis(

        host=settings.REDIS_HOST,

        port=settings.REDIS_PORT,

        decode_responses=True

    )

    try:
        await redis_client.ping()
        print("Redis Connected")
    except (RedisConnectionError, OSError) as exc:
        logger.warning(
            "Redis unavailable at %s:%s; continuing without Redis. %s",
            settings.REDIS_HOST,
            settings.REDIS_PORT,
            exc,
        )
        redis_client = None


async def close_redis_connection():

    if redis_client is None:
        return

    await redis_client.close()

    print("Redis Closed")