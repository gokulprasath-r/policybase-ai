from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    input: str = Field(min_length=1)


class Source(BaseModel):
    filename: str
    page: int


class ChatResponse(BaseModel):
    result: str
    sources: list[Source]


class LLMResponse(BaseModel):
    answer: str
    has_answer: bool
