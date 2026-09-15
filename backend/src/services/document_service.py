from fastapi import UploadFile, HTTPException
import os
import shutil

from src.database.database import document_collection
from src.services.pdf_service import extract_text
from src.services.chunk_service import chunk_text
from src.services.vector_service import upsertVector
async def upload_document(file: UploadFile):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    os.makedirs("../documents", exist_ok=True)

    file_path = f"../documents/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_path": file_path
    }

    result = await document_collection.insert_one(document)

    text = await extract_text(file_path)

    chunks = chunk_text(text)

    l = upsertVector(chunks, file.filename)




    return {
        "message": "Document uploaded successfully",
        "document_id": str(result.inserted_id),
        "filename": file.filename
    }
