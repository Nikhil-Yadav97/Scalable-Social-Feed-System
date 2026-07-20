import asyncio

from app.db.mongodb import connect_to_mongodb
from app.workers.feed_worker import start_worker
from app.db.redis import connect_to_redis

async def main():

    await connect_to_mongodb()
    await connect_to_redis()

    print("Feed Worker Started")

    await start_worker()


asyncio.run(main())