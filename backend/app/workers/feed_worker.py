import json
import logging

from bson import ObjectId

from app.db.mongodb import posts, follows, feeds
import app.db.redis as redis_db


logger = logging.getLogger(__name__)


async def process_job(job):

    author_id = ObjectId(job["author_id"])
    post_id = ObjectId(job["post_id"])

    # Fetch post
    post = await posts.find_one(
        {
            "_id": post_id
        }
    )

    if post is None:
        return

    cursor = follows.find(
        {
            "followee_id": author_id
        }
    )

    async for follow in cursor:

        follower_id = follow["follower_id"]

        # Update follower's feed
        await feeds.update_one(
            {
                "user_id": follower_id
            },
            {
                "$push": {
                    "posts": {
                        "$each": [
                            {
                                "post_id": post_id,
                                "created_at": post["created_at"]
                            }
                        ],
                        "$position": 0,
                        "$slice": 500
                    }
                }
            },
            upsert=True
        )

        # Invalidate cached first page
        if redis_db.redis_client is not None:

            await redis_db.redis_client.delete(
                f"feed:{str(follower_id)}"
            )


async def start_worker():

    if redis_db.redis_client is None:
        raise RuntimeError("Redis is not connected.")

    while True:

        try:

            _, data = await redis_db.redis_client.blpop(
                "feed_queue"
            )

            job = json.loads(data)

            await process_job(job)

        except Exception as e:

            logger.exception(f"Worker error: {e}")