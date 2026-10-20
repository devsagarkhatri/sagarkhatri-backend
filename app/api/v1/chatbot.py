
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chatbot.chat import ChatRequest, ChatResponse
from app.services.chatbot.agent_service import answer_portfolio_question
from app.services.chatbot.chatbot_cache import (
    cache_answer,
    get_cached_answer,
)
from app.services.chatbot.openrouter_service import OpenRouterServiceError
from app.services.chatbot.rate_limit import enforce_chat_rate_limit


router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post(
    "",
    response_model=ChatResponse,
    dependencies=[Depends(enforce_chat_rate_limit)],
)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
) -> ChatResponse:
    question = request.message.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Message cannot be empty.",
        )

    cached_answer = get_cached_answer(question)

    if cached_answer is not None:
        return ChatResponse(answer=cached_answer)

    try:
        answer = await answer_portfolio_question(
            db=db,
            question=question,
        )

        # Cache only successful answers.
        cache_answer(question, answer)

        return ChatResponse(answer=answer)

    except OpenRouterServiceError:
        raise HTTPException(
            status_code=503,
            detail=(
                "The portfolio assistant is temporarily unavailable. "
                "Please try again later."
            ),
        )
