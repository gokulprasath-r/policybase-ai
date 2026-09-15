from fastapi import APIRouter, UploadFile, File, status

from src.services.document_service import upload_document,get_all_documents,get_document,delete_document
from src.schemas.document_schema import DocumentResponse,DocumentMetaResponse,DocumentDeleteResponse

router = APIRouter(
    prefix="/admin/documents",
    tags=["Documents"]
)

@router.post("/upload",status_code=status.HTTP_200_OK,response_model=DocumentResponse)
async def upload(file: UploadFile = File(...)):
    return await upload_document(file)

@router.get("/", response_model=list[DocumentMetaResponse])
async def get_documents():
    return await get_all_documents()

@router.get("/{document_id}", response_model=DocumentMetaResponse)
async def get_document_by_id(document_id: str):
    return await get_document(document_id)

@router.delete("/{document_id}",response_model=DocumentDeleteResponse)
async def delete_document_by_id(document_id: str):
    return await delete_document(document_id)
