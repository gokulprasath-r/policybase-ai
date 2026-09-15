from fastapi import APIRouter,status
from src.schemas.chat_schema import ChatResponse,ChatRequest
from src.services.retrival_service import retrive_answer
from src.services.embedding_service import generate_embedding
from src.services.llm_service import generate_answer

router = APIRouter()

@router.post("/chat",status_code=status.HTTP_200_OK)
async def chat(input):
    user_query_vector = generate_embedding(input)
    retrieval = retrive_answer(user_query_vector)

    if retrieval is None:
        return {
            "result": "I don't have information about that.",
            "sources": []
        }

    ans = generate_answer(
            input,
            retrieval["context"]
        )

    return {
        "result": ans.answer,
        "sources": retrieval["sources"] if ans.has_answer else []
    }
