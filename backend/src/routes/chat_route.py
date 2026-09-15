from fastapi import APIRouter, status, HTTPException
from src.schemas.chat_schema import ChatResponse, ChatRequest
from src.services.retrival_service import retrive_answer
from src.services.embedding_service import generate_embedding
from src.services.llm_service import generate_answer, generate_search_query
from src.services.chat_history_service import get_history, add_message
from src.utils.logger import logger


router = APIRouter()


@router.post(
    "/chat",
    status_code=status.HTTP_200_OK,
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    logger.info(
        "Chat request received for session: %s",
        request.session_id
    )

    try:
        history = get_history(request.session_id)







        search_query = generate_search_query(
            request.input,
            history
        )
        print(search_query)
        add_message(
            request.session_id,
            "user",
            request.input
        )

        user_query_vector = generate_embedding(search_query)

        retrieval = retrive_answer(user_query_vector)

        # if retrieval is None:

        #     answer = "I don't have information about that."

        #     add_message(
        #         request.session_id,
        #         "assistant",
        #         answer
        #     )

        #     return {
        #         "result": answer,
        #         "sources": []
        #     }

        ans = generate_answer(
            request.input,
            retrieval["context"],
            history
        )

        add_message(
            request.session_id,
            "assistant",
            ans.answer
        )

        return {
            "result": ans.answer,
            "sources": retrieval["sources"] if ans.has_answer else []
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing your request."
        )
