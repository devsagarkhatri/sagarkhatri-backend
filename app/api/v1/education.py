
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security.admin import require_admin
from app.schemas.education import (
    EducationCreate,
    EducationResponse,
    EducationUpdate,
)
from app.services.education_service import (
    get_education,
    get_all_education,
    get_education_by_id,
    create_education,
    update_education,
    delete_education,
)

router = APIRouter(prefix="/education", tags=["Education"])


@router.get("", response_model=list[EducationResponse])
def list_education(db: Session = Depends(get_db)):
    return get_education(db)


@router.get("/admin", response_model=list[EducationResponse])
def admin_list_education(
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return get_all_education(db)


@router.get("/admin/{record_id}", response_model=EducationResponse)
def admin_get_education(
    record_id: UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_education_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Education record not found")
    return record


@router.post("", response_model=EducationResponse, status_code=201)
def admin_create_education(
    payload: EducationCreate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return create_education(db, payload.model_dump())


@router.patch("/{record_id}", response_model=EducationResponse)
def admin_update_education(
    record_id: UUID,
    payload: EducationUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_education_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Education record not found")

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    return update_education(db, record, changes)


@router.delete("/{record_id}", status_code=204)
def admin_delete_education(
    record_id: UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_education_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Education record not found")

    delete_education(db, record)
    return None