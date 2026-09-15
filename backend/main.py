from fastapi import FastAPI,status
from src.routes.document_route import router as document_router
app = FastAPI()

@app.get("/",status_code=status.HTTP_200_OK)
def main():
    return "Welcome to PolicyBase AI API"

app.include_router(document_router)
