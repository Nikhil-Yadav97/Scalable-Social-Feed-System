from datetime import datetime, timezone
import json

from bson import ObjectId

import app.db.redis as redis_db
from app.db.mongodb import posts, users


async def create_post(current_user, post_data):

    author = await users.find_one(
        {
            "_id": ObjectId(current_user["id"])
        }
    )

    if author is None:
        raise ValueError("User not found")

    document = {
        "author_id": author["_id"],
        "content": post_data.content,
        "created_at": datetime.now(timezone.utc),
        "like_count": 0,
        "comment_count": 0
    }

    result = await posts.insert_one(document)

    await users.update_one(
        {
            "_id": author["_id"]
        },
        {
            "$inc": {
                "post_count": 1
            }
        }
    )

    # Fan-Out-on-Write only for normal users
    if not author.get("is_celebrity", False):

        job = {
            "post_id": str(result.inserted_id),
            "author_id": str(author["_id"])
        }

        if redis_db.redis_client is not None:
            await redis_db.redis_client.rpush(
                "feed_queue",
                json.dumps(job)
            )

    return {
        "message": "Post created successfully",
        "post_id": str(result.inserted_id),
        "fanout_strategy": (
            "fan_out_on_read"
            if author.get("is_celebrity", False)
            else "fan_out_on_write"
        )
    }