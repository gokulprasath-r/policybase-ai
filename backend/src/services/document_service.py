from fastapi import UploadFile, HTTPException, File
from pathlib import Path
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone

from src.database.database import document_collection
from src.services.pdf_service import extract_text
from src.services.chunk_service import chunk_text
from src.services.vector_service import upsert_vector, delete_vectors
from src.services.storage_service import upload_file, download_file, delete_file
from src.utils.logger import logger
from fastapi.responses import Response

async def upload_document(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

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

    MAX_FILE_SIZE = 10 * 1024 * 1024

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB"
        )

    file_id = None

    try:
        # Store PDF in MongoDB GridFS
        file_id = await upload_file(
            filename,
            file_content,
            file.content_type
        )

        logger.info("File stored in GridFS: %s", filename)

        # Extract PDF text directly from GridFS
        pdf_content = await download_file(str(file_id))

        text = await extract_text(pdf_content)

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

        # Store embeddings in Pinecone
        upsert_vector(chunks, filename)

        logger.info(
            "Document indexed successfully: %s",
            filename
        )

        document = {
            "filename": filename,
            "content_type": file.content_type,
            "file_id": str(file_id),
            "status": "indexed",
            "uploaded_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }

        result = await document_collection.insert_one(document)

        return {
            "message": "Document uploaded successfully",
            "document_id": str(result.inserted_id),
            "filename": filename
        }

    except HTTPException:
        if file_id:
            await delete_file(str(file_id))

        logger.warning(
            "Document upload rejected: %s",
            filename
        )

        raise

    except Exception:
        if file_id:
            await delete_file(str(file_id))

        logger.exception(
            "Document upload failed: %s",
            filename
        )

        raise


async def get_all_documents():

    documents = await document_collection.find().to_list(length=None)

    return [
        {
            "document_id": str(document["_id"]),
            "filename": document["filename"],
            "content_type": document["content_type"],
            "file_id": document["file_id"],
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
        "file_id": document["file_id"],
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

    # Delete PDF from GridFS
    await delete_file(document["file_id"])

    # Delete vectors from Pinecone
    delete_vectors(document["filename"])

    # Delete metadata from MongoDB
    await document_collection.delete_one({
        "_id": object_id
    })

    logger.info(
        "Document deleted successfully: %s",
        document["filename"]
    )

    return {
        "message": "Document deleted successfully"
    }



async def get_document_file(document_id: str):

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

    try:
        file_content = await download_file(
            document["file_id"]
        )

    except Exception:
        raise HTTPException(
            status_code=404,
            detail="PDF file not found"
        )

    return Response(
        content=file_content,
        media_type=document["content_type"],
        headers={
            "Content-Disposition": f'inline; filename="{document["filename"]}"'
        }
    )
