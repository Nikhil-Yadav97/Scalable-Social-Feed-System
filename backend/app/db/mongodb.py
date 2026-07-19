from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

database = client[settings.DATABASE_NAME]

# Collections
users = database["users"]
posts = database["posts"]
follows = database["follows"]
feeds = database["feeds"]


async def connect_to_mongodb():
    await client.server_info()
    print("MongoDB Connected")


async def close_mongodb_connection():
    client.close()
    print("MongoDB Closed")