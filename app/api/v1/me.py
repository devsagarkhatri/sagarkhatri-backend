from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.me import MeResponse
from app.services.me_service import get_public_portfolio


router = APIRouter(
    prefix="/me",
    tags=["Portfolio"],
)


@router.get(
    "",
    response_model=MeResponse,
)
def read_public_portfolio(
    db: Session = Depends(get_db),
):
    try:
        return get_public_portfolio(db)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )