from fastapi import FastAPI,status
from src.routes.document_route import router as document_router
from src.routes.chat_route import router as chat_router
app = FastAPI()

@app.get("/",status_code=status.HTTP_200_OK)
def main():
    return "Welcome to PolicyBase AI API"

app.include_router(document_router)
app.include_router(chat_router)
