from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv();
# Automatically picks up PINECONE_API_KEY from the environment
pc = Pinecone()
MY_INDEX_NAME = os.getenv("MY_INDEX_NAME")
index = pc.Index(MY_INDEX_NAME)

print(f"You are connected to: {MY_INDEX_NAME}")
