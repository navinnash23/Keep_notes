from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None

async def connect_to_mongo():
    try:
        MongoDB.client = AsyncIOMotorClient(settings.MONGODB_URL)
        # Wait for MongoDB to be fully connected by pinging
        await MongoDB.client.admin.command('ping')
        print("MongoDB connection successful.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    if MongoDB.client:
        MongoDB.client.close()
        print("MongoDB connection closed.")

def get_database():
    if MongoDB.client is None:
        raise ValueError("MongoDB client is not connected. Please ensure the connection is established.")
    return MongoDB.client[settings.DATABASE_NAME]
