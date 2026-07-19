from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

database = client[settings.DATABASE_NAME]

async def connect_to_mongodb():
    """Establish a MongoDB connection and verify it."""
    await client.server_info()
    print("MongoDB Connected")


async def close_mongodb_connection():
    """Close the MongoDB client connection."""
    client.close()
    print("MongoDB Closed")