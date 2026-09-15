from src.database.pinecone import index


def retrive_answer(query_vector):
    result = index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True
    )

    contexts = []
    sources = []

    for match in result.matches:
        if match.score >= 0.65: # include the chunk
            contexts.append(match.metadata["text"])

            source = {
                "filename": match.metadata["filename"],
                "page": match.metadata["page"]
            }

            if source not in sources:
                sources.append(source)

    if not contexts:
        return None

    return {
        "context": "\n\n".join(contexts),
        "sources": sources
    }
