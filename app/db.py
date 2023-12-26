# File: app/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.constants.db import MONGODB_URL, DATABASE_NAME

def get_database() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    return database