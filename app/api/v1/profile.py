from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.security.admin import require_admin
from app.services.profile_service import get_profile, update_profile
from app.services.chatbot.chatbot_cache import clear_chatbot_cache

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.get(
    "",
    response_model=ProfileResponse,
)
def read_profile(
    db: Session = Depends(get_db),
):
    profile = get_profile(db)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return profile


@router.patch(
    "",
    response_model=ProfileResponse,
)
def edit_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="No profile fields provided",
        )

    profile = update_profile(db, changes)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    clear_chatbot_cache()
    return profile