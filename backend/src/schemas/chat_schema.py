from pydantic import BaseModel

class ChatRequest(BaseModel):
    input: str

class ChatResponse(BaseModel):
    result:str
    sources: list


class LLMResponse(BaseModel):
    answer: str
    has_answer: bool
