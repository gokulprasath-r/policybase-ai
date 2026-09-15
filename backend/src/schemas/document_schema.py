from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):
    message: str
    document_id: str
    filename:str


class DocumentMetaResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    file_path: str
    status: str
    uploaded_at: datetime

class DocumentDeleteResponse(BaseModel):
    message: str
