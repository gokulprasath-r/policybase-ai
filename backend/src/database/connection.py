import os
from pymongo import AsyncMongoClient
from dotenv import load_dotenv

load_dotenv();
MONGO_URI = os.getenv("MONGO_URI")

client = AsyncMongoClient(MONGO_URI)
db = client["policybaseai"]
