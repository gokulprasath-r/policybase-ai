from pymongo import AsyncMongoClient
from src.config import MONGO_URI

client = AsyncMongoClient(MONGO_URI)
db = client["policybaseai"]
