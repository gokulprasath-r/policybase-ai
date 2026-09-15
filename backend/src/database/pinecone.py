from pinecone import Pinecone
from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
print(f"You are connected to: {PINECONE_INDEX_NAME}")
