from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.site_sections import SiteSectionCreate, SiteSectionResponse, SiteSectionUpdate
from app.security.admin import require_admin
from app.services.site_section_service import (
    get_site_sections,
    get_all_site_sections,
    get_site_section,
    create_site_section,
    update_site_section,
    delete_site_section,
)

router = APIRouter(prefix='/site-sections', tags=['Site Sections'])


@router.get("", response_model=list[SiteSectionResponse])
def read_site_sections(db: Session = Depends(get_db)):
    """Public: return visible records."""
    return get_site_sections(db)


@router.get("/admin", response_model=list[SiteSectionResponse])
def read_all_site_sections(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: return visible and hidden records."""
    return get_all_site_sections(db)


@router.get("/admin/{record_id}", response_model=SiteSectionResponse)
def read_site_section_by_id(
    record_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    record = get_site_section(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail='Site Section' + " not found")
    return record


@router.post("", response_model=SiteSectionResponse, status_code=status.HTTP_201_CREATED)
def add_site_section(
    payload: SiteSectionCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    try:
        return create_site_section(db, payload.model_dump())
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="A record with a conflicting unique value may already exist") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to create record") from exc


@router.patch("/{record_id}", response_model=SiteSectionResponse)
def edit_site_section(
    record_id: UUID,
    payload: SiteSectionUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided")
    try:
        record = update_site_section(db, record_id, changes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="A record with a conflicting unique value may already exist") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to update record") from exc
    if record is None:
        raise HTTPException(status_code=404, detail='Site Section' + " not found")
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_site_section(
    record_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    try:
        deleted = delete_site_section(db, record_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to delete record") from exc
    if not deleted:
        raise HTTPException(status_code=404, detail='Site Section' + " not found")
    return None
