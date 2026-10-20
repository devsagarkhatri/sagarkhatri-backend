
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.experience import (
    ExperienceCreate,
    ExperienceResponse,
    ExperienceUpdate,
)
from app.security.admin import require_admin
from app.services.experience_service import (
    create_experience,
    delete_experience,
    get_all_experiences,
    get_experience,
    get_experiences,
    update_experience,
)
from app.services.chatbot.chatbot_cache import clear_chatbot_cache


router = APIRouter(
    prefix="/experience",
    tags=["Experience"],
)


@router.get(
    "",
    response_model=list[ExperienceResponse],
)
def read_experience(
    db: Session = Depends(get_db),
):
    """Public: return visible experiences."""
    return get_experiences(db)


@router.get(
    "/admin",
    response_model=list[ExperienceResponse],
)
def read_all_experiences(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: return visible and hidden experiences."""
    return get_all_experiences(db)


@router.get(
    "/admin/{experience_id}",
    response_model=ExperienceResponse,
)
def read_experience_by_id(
    experience_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: retrieve one experience, including hidden records."""
    experience = get_experience(db, experience_id)

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )

    return experience


@router.post(
    "",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_experience(
    payload: ExperienceCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: create an experience and its points."""
    try:
        experience = create_experience(
            db,
            payload.model_dump(),
        )
        clear_chatbot_cache()
        return experience
    except Exception:
        # The service has already rolled back the failed transaction.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create experience",
        )


@router.patch(
    "/{experience_id}",
    response_model=ExperienceResponse,
)
def edit_experience(
    experience_id: UUID,
    payload: ExperienceUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: partially update an experience."""
    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No experience fields provided",
        )

    try:
        experience = update_experience(
            db,
            experience_id,
            changes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update experience",
        )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )

    clear_chatbot_cache()
    return experience


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_experience(
    experience_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: delete an experience and its points."""
    try:
        deleted = delete_experience(db, experience_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete experience",
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )

    clear_chatbot_cache()
    return None