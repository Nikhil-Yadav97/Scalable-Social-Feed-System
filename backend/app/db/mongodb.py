from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


client = AsyncIOMotorClient(settings.MONGO_URI)

database = client[settings.DATABASE_NAME]

# Collections
users = database["users"]
posts = database["posts"]
follows = database["follows"]
feeds = database["feeds"]
likes = database["likes"]


async def connect_to_mongodb():

    await client.server_info()

    # ----------------------------
    # Users
    # ----------------------------
    await users.create_index(
        "username",
        unique=True
    )

    await users.create_index(
        "email",
        unique=True
    )

    await users.create_index(
        "followers_count"
    )

    await users.create_index(
        "is_celebrity"
    )

    # ----------------------------
    # Posts
    # ----------------------------
    await posts.create_index(
        "author_id"
    )

    await posts.create_index(
        [
            ("author_id", 1),
            ("created_at", -1)
        ]
    )

    await posts.create_index(
        "created_at"
    )

    # ----------------------------
    # Follows
    # ----------------------------
    await follows.create_index(
        [
            ("follower_id", 1),
            ("followee_id", 1)
        ],
        unique=True
    )

    await follows.create_index(
        "followee_id"
    )

    await follows.create_index(
        "follower_id"
    )

    # ----------------------------
    # Feeds
    # ----------------------------
    await feeds.create_index(
        "user_id",
        unique=True
    )

    # ----------------------------
    # Likes
    # ----------------------------
    await likes.create_index(
        [
            ("user_id", 1),
            ("post_id", 1)
        ],
        unique=True
    )

    await likes.create_index(
        "post_id"
    )

    await likes.create_index(
        "user_id"
    )

    print("MongoDB Connected")


async def close_mongodb_connection():

    client.close()

    print("MongoDB Closed")