from fastapi import UploadFile, HTTPException,File
import os
from pathlib import Path
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone
from src.database.database import document_collection
from src.services.pdf_service import extract_text
from src.services.chunk_service import chunk_text
from src.services.vector_service import upsert_vector
from src.utils.logger import logger
from src.services.vector_service import delete_vectors

async def upload_document(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    os.makedirs("../documents", exist_ok=True)
    filename = Path(file.filename or "").name

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    if Path(filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )


    existing_document = await document_collection.find_one({
        "filename": filename
    })

    if existing_document:
        raise HTTPException(
            status_code=409,
            detail="A document with this filename already exists"
        )

    logger.info("Document upload started: %s", filename)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB"
        )

    file_path = f"../documents/{filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    document = {
        "filename": filename,
        "content_type": file.content_type,
        "file_path": file_path,
        "status": "indexed",
        "uploaded_at": datetime.now(timezone.utc),
         "updated_at": datetime.now(timezone.utc)
    }

    try:
        text = await extract_text(file_path)

        if not any(page.strip() for page in text):
            raise HTTPException(
                status_code=400,
                detail="The PDF does not contain extractable text"
            )

        chunks = chunk_text(text)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Could not generate chunks from the PDF"
            )

        upsert_vector(chunks, filename)
        logger.info("Document indexed successfully: %s", filename)
    except HTTPException:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.warning("Document upload rejected: %s", filename)
        raise

    except Exception:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.exception("Document upload failed: %s", filename)
        raise

    result = await document_collection.insert_one(document)

    return {
        "message": "Document uploaded successfully",
        "document_id": str(result.inserted_id),
        "filename": filename
    }



async def get_all_documents():
    documents = await document_collection.find().to_list(length=None)

    return [
        {
            "document_id": str(document["_id"]),
            "filename": document["filename"],
            "content_type": document["content_type"],
            "file_path": document["file_path"],
            "status": document["status"],
             "uploaded_at": document["uploaded_at"],
             "updated_at": document["updated_at"]
        }
        for document in documents
    ]




async def get_document(document_id: str):
    try:
        object_id = ObjectId(document_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID"
        )

    document = await document_collection.find_one({
        "_id": object_id
    })

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "document_id": str(document["_id"]),
        "filename": document["filename"],
        "content_type": document["content_type"],
        "file_path": document["file_path"],
        "status": document["status"],
         "uploaded_at": document["uploaded_at"],
         "updated_at": document["updated_at"]
    }


async def delete_document(document_id: str):
    try:
        object_id = ObjectId(document_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID"
        )

    document = await document_collection.find_one({
        "_id": object_id
    })

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    if os.path.exists(document["file_path"]):
        os.remove(document["file_path"])

    delete_vectors(document["filename"])

    await document_collection.delete_one({
        "_id": object_id
    })

    return {
        "message": "Document deleted successfully"
    }
