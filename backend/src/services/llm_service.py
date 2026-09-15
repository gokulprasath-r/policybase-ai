from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from src.schemas.chat_schema import LLMResponse
from src.utils.logger import logger
from src.config import GROQ_API_KEY

llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=GROQ_API_KEY
    )

structured_llm = llm.with_structured_output(LLMResponse)

def generate_search_query(question, history):

    prompt = f"""
    Convert the user's latest question into a standalone search query.
    Conversation history:{history}
    Latest question:{question}
    Return only the standalone search query.
    """

    response = llm.invoke(prompt)
    logger.info("Generating standalone search query")
    return response.content

def generate_answer(question, context,history):

    prompt = f"""
                You are a company policy assistant.
                Answer the user's question using the information in the context below.
                history:{history}
                Context:{context}
                Question:{question}
                Do not make up or assume information.
                If the context does not contain enough information to answer the question,set has_answer to false and answer to I don't have information about that.
                Return JSON in this format:

                {{
                    "answer": "your answer",
                    "has_answer": true
                }}
            """

    logger.info("Generating answer using LLM")
    return structured_llm.invoke(prompt);
