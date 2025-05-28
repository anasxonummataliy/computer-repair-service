from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

# Global database instance
db_instance = MongoDB()

async def connect_to_mongodb(uri: str = "mongodb://localhost:27017", database_name: str = "service"):
    """MongoDB ga ulanish"""
    try:
        db_instance.client = AsyncIOMotorClient(uri)
        db_instance.database = db_instance.client[database_name]
        
        # Connection test
        await db_instance.client.admin.command('ping')
        print("MongoDB ga muvaffaqiyatli ulandi")
        return db_instance.database
    except Exception as e:
        print(f"MongoDB ga ulanishda xatolik: {e}")
        raise

async def close_mongodb_connection():
    """MongoDB ulanishini yopish"""
    if db_instance.client:
        db_instance.client.close()
        print("MongoDB ulanishi yopildi")

def get_database():
    """Database instance ni olish"""
    if db_instance.database is None:
        raise Exception("Database ulanishi o'rnatilmagan")
    return db_instance.database

def get_collection(collection_name: str):
    """Collection ni olish"""
    db = get_database()
    return db[collection_name]
