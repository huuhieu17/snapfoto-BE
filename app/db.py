# File: app/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase

MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "mydatabase"

def get_database() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    return database