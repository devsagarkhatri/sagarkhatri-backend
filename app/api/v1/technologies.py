from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.technology import TechnologyCreate, TechnologyResponse, TechnologyUpdate
from app.security.admin import require_admin
from app.services.technology_service import (
    get_technologies,
    get_all_technologies,
    get_technology,
    create_technology,
    update_technology,
    delete_technology,
)
from app.services.chatbot.chatbot_cache import clear_chatbot_cache


router = APIRouter(prefix='/technologies', tags=['Technologies'])


@router.get("", response_model=list[TechnologyResponse])
def read_technologies(db: Session = Depends(get_db)):
    """Public: return visible records."""
    return get_technologies(db)


@router.get("/admin", response_model=list[TechnologyResponse])
def read_all_technologies(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: return visible and hidden records."""
    return get_all_technologies(db)


@router.get("/admin/{record_id}", response_model=TechnologyResponse)
def read_technology_by_id(
    record_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    record = get_technology(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail='Technology' + " not found")
    return record


@router.post("", response_model=TechnologyResponse, status_code=status.HTTP_201_CREATED)
def add_technology(
    payload: TechnologyCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    try:
        record = create_technology(db, payload.model_dump())
        clear_chatbot_cache()
        return record
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="A record with a conflicting unique value may already exist") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to create record") from exc


@router.patch("/{record_id}", response_model=TechnologyResponse)
def edit_technology(
    record_id: UUID,
    payload: TechnologyUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided")
    try:
        record = update_technology(db, record_id, changes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="A record with a conflicting unique value may already exist") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to update record") from exc
    if record is None:
        raise HTTPException(status_code=404, detail='Technology' + " not found")
    clear_chatbot_cache()
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_technology(
    record_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    try:
        deleted = delete_technology(db, record_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to delete record") from exc
    if not deleted:
        raise HTTPException(status_code=404, detail='Technology' + " not found")
    clear_chatbot_cache()
    return None
