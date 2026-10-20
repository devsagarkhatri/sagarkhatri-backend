
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
        description="The visitor's message to the portfolio chatbot.",
    )


class ChatResponse(BaseModel):
    answer: str
