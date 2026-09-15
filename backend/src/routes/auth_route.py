from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.config import ADMIN_PASSWORD

router = APIRouter(prefix="/admin", tags=["Admin"])


class AdminLoginRequest(BaseModel):
    password: str


@router.post("/auth")
async def admin_auth(request: AdminLoginRequest):

    if request.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin password"
        )

    return {
        "authenticated": True
    }
