from bson import ObjectId

from app.db.mongodb import feeds, posts, follows, users

import json

import app.db.redis as redis_db
async def get_feed(user_id: str, page: int = 1, limit: int = 10):
    cache_key = f"feed:{user_id}"

    if page == 1 and redis_db.redis_client is not None:

        cached_feed = await redis_db.redis_client.get(cache_key)

        if cached_feed:

            return json.loads(cached_feed)
    # ----------------------------
    # Precomputed feed (Fan-Out-on-Write)
    # ----------------------------
    feed = await feeds.find_one(
        {
            "user_id": ObjectId(user_id)
        }
    )

    feed_posts = feed["posts"] if feed else []

    # ----------------------------
    # Celebrity posts (Fan-Out-on-Read)
    # ----------------------------
    follow_cursor = follows.find(
        {
            "follower_id": ObjectId(user_id)
        }
    )

    followed_ids = []

    async for follow in follow_cursor:
        followed_ids.append(follow["followee_id"])

    celebrity_posts = []

    if followed_ids:

        celebrity_cursor = users.find(
            {
                "_id": {
                    "$in": followed_ids
                },
                "is_celebrity": True
            }
        )

        celebrity_ids = []

        async for user in celebrity_cursor:
            celebrity_ids.append(user["_id"])

        if celebrity_ids:

            cursor = posts.find(
                {
                    "author_id": {
                        "$in": celebrity_ids
                    }
                }
            ).sort("created_at", -1)

            docs = await cursor.to_list(length=100)

            celebrity_posts = [
                {
                    "post_id": post["_id"],
                    "created_at": post["created_at"]
                }
                for post in docs
            ]

    # ----------------------------
    # Merge
    # ----------------------------
    merged = feed_posts + celebrity_posts

    # ----------------------------
    # Remove duplicates
    # ----------------------------
    unique = {}

    for post in merged:
        unique[str(post["post_id"])] = post

    merged = list(unique.values())

    # ----------------------------
    # Sort newest first
    # ----------------------------
    merged.sort(
        key=lambda x: x["created_at"],
        reverse=True
    )

    # ----------------------------
    # Pagination
    # ----------------------------
    start = (page - 1) * limit
    end = start + limit

    merged = merged[start:end]

    if not merged:
        return []

    # ----------------------------
    # Fetch post details
    # ----------------------------
    post_ids = [
        item["post_id"]
        for item in merged
    ]

    cursor = posts.find(
        {
            "_id": {
                "$in": post_ids
            }
        }
    )

    documents = await cursor.to_list(length=None)

    lookup = {
        str(post["_id"]): post
        for post in documents
    }

    result = []

    for item in merged:

        post = lookup.get(str(item["post_id"]))

        if post is None:
            continue

        result.append(
            {
                "id": str(post["_id"]),
                "author_id": str(post["author_id"]),
                "content": post["content"],
                "created_at": post["created_at"],
                "like_count": post["like_count"],
                "comment_count": post["comment_count"]
            }
        )

        if page == 1 and redis_db.redis_client is not None:

        await redis_db.redis_client.setex(
            cache_key,
            300,
            json.dumps(
                result,
                default=str
            )
        )

    return result