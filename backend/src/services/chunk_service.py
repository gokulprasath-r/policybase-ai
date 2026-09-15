from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = []

    for page_number, page_text in enumerate(pages, start=1):
        page_chunks = splitter.split_text(page_text)

        for chunk in page_chunks:
            chunks.append({
                "text": chunk,
                "page": page_number
            })

    return chunks
