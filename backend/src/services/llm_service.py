from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from src.schemas.chat_schema import LLMResponse

def generate_answer(question, context):
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )

    structured_llm = llm.with_structured_output(LLMResponse)

    prompt = f"""
                You are a company policy assistant.
                Answer the user's question using the information in the context below.
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

    return structured_llm.invoke(prompt);
