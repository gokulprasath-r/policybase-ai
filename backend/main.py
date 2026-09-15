from fastapi import FastAPI,status,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.config import FRONTEND_URL
from src.routes.document_route import router as document_router
from src.routes.chat_route import router as chat_router
from src.routes.auth_route import router as auth_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health",status_code=status.HTTP_200_OK)
async def health():
    return {
        "status": "ok"
    }

app.include_router(document_router)
app.include_router(chat_router)
app.include_router(auth_router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )
