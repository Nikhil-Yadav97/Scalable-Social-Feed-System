from datetime import datetime, timezone
from bson import ObjectId

from app.db.mongodb import follows, users


async def follow_user(current_user_id: str, followee_id: str):

    if current_user_id == followee_id:
        raise ValueError("You cannot follow yourself")

    # Check user exists
    followee = await users.find_one(
        {
            "_id": ObjectId(followee_id)
        }
    )

    if followee is None:
        raise ValueError("User not found")

    # Already following?
    existing = await follows.find_one(
        {
            "follower_id": ObjectId(current_user_id),
            "followee_id": ObjectId(followee_id)
        }
    )

    if existing:
        raise ValueError("Already following this user")

    await follows.insert_one(
        {
            "follower_id": ObjectId(current_user_id),
            "followee_id": ObjectId(followee_id),
            "created_at": datetime.now(timezone.utc)
        }
    )

    # Update counters
    await users.update_one(
        {"_id": ObjectId(current_user_id)},
        {"$inc": {"following_count": 1}}
    )

    await users.update_one(
        {"_id": ObjectId(followee_id)},
        {"$inc": {"followers_count": 1}}
    )

    return {"message": "Followed successfully"}


async def unfollow_user(current_user_id: str, followee_id: str):

    if current_user_id == followee_id:
        raise ValueError("You cannot unfollow yourself")

    existing = await follows.find_one(
        {
            "follower_id": ObjectId(current_user_id),
            "followee_id": ObjectId(followee_id)
        }
    )

    if existing is None:
        raise ValueError("You are not following this user")

    await follows.delete_one(
        {
            "_id": existing["_id"]
        }
    )

    await users.update_one(
        {
            "_id": ObjectId(current_user_id)
        },
        {
            "$inc": {
                "following_count": -1
            }
        }
    )

    await users.update_one(
        {
            "_id": ObjectId(followee_id)
        },
        {
            "$inc": {
                "followers_count": -1
            }
        }
    )

    return {
        "message": "Unfollowed successfully"
    }