from motor.motor_asyncio import AsyncIOMotorClient
from config.config import settings


client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]


print("connect to database successfully")



