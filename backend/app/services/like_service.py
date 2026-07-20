from datetime import datetime, timezone

from bson import ObjectId

from app.db.mongodb import likes, posts


async def like_post(current_user_id: str, post_id: str):

    # Check post exists
    post = await posts.find_one(
        {
            "_id": ObjectId(post_id)
        }
    )

    if post is None:
        raise ValueError("Post not found")

    # Already liked?
    existing = await likes.find_one(
        {
            "user_id": ObjectId(current_user_id),
            "post_id": ObjectId(post_id)
        }
    )

    if existing:
        raise ValueError("You have already liked this post")

    # Insert like
    await likes.insert_one(
        {
            "user_id": ObjectId(current_user_id),
            "post_id": ObjectId(post_id),
            "created_at": datetime.now(timezone.utc)
        }
    )

    # Increment like count
    await posts.update_one(
        {
            "_id": ObjectId(post_id)
        },
        {
            "$inc": {
                "like_count": 1
            }
        }
    )

    return {
        "message": "Post liked successfully"
    }


async def unlike_post(current_user_id: str, post_id: str):

    existing = await likes.find_one(
        {
            "user_id": ObjectId(current_user_id),
            "post_id": ObjectId(post_id)
        }
    )

    if existing is None:
        raise ValueError("You have not liked this post")

    await likes.delete_one(
        {
            "_id": existing["_id"]
        }
    )

    await posts.update_one(
        {
            "_id": ObjectId(post_id)
        },
        {
            "$inc": {
                "like_count": -1
            }
        }
    )

    return {
        "message": "Post unliked successfully"
    }


async def get_post_likes(post_id: str):

    cursor = likes.find(
        {
            "post_id": ObjectId(post_id)
        }
    )

    users = []

    async for like in cursor:

        users.append(
            str(like["user_id"])
        )

    return {
        "count": len(users),
        "users": users
    }


async def has_liked(current_user_id: str, post_id: str):

    existing = await likes.find_one(
        {
            "user_id": ObjectId(current_user_id),
            "post_id": ObjectId(post_id)
        }
    )

    return existing is not None