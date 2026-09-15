from fastapi import APIRouter, UploadFile, File, status

from src.services.document_service import upload_document
from src.schemas.document_schema import DocumentResponse

router = APIRouter(
    prefix="/admin/documents",
    tags=["Documents"]
)

@router.post("/upload",status_code=status.HTTP_200_OK,response_model=DocumentResponse)
async def upload(file: UploadFile = File(...)):
    return await upload_document(file)
