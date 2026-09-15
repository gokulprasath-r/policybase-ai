import asyncio

from src.database.database import document_collection
from src.database.pinecone import index


async def clean_mongodb():
    result = await document_collection.delete_many({})
    print(f"MongoDB: deleted {result.deleted_count} documents")


def clean_pinecone():
    index.delete(delete_all=True)
    print("Pinecone: all vectors deleted")


async def main():
    await clean_mongodb()
    clean_pinecone()


asyncio.run(main())
