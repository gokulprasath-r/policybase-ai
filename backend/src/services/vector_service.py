from src.database.pinecone import index
from src.services.embedding_service import generate_embedding
import os

def upsert_vector(chunks,filename):

    for i,chunk in enumerate(chunks, start=1):
        vector = generate_embedding(chunk["text"])
        index.upsert(
                    vectors=[
                        {
                            "id":  f"{os.path.splitext(filename)[0]}-page{chunk['page']}-chunk{i}",
                            "values": vector,
                            "metadata": {
                                "text": chunk["text"],
                                "page": chunk["page"],
                                "filename": filename
                            }
                        }
                    ]
                )
    return index


def delete_vectors(filename: str):
    result = index.delete(
        filter={
            "filename": filename
        }
    )

    return result
