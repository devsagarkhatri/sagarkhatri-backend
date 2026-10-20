
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security.admin import require_admin
from app.schemas.certification import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
)
from app.services.certification_service import (
    get_certifications,
    get_all_certifications,
    get_certification_by_id,
    create_certification,
    update_certification,
    delete_certification,
)

router = APIRouter(prefix="/certifications", tags=["Certifications"])


@router.get("", response_model=list[CertificationResponse])
def list_certifications(db: Session = Depends(get_db)):
    return get_certifications(db)


@router.get("/admin", response_model=list[CertificationResponse])
def admin_list_certifications(
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return get_all_certifications(db)


@router.get("/admin/{record_id}", response_model=CertificationResponse)
def admin_get_certification(
    record_id: UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_certification_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Certification not found")
    return record


@router.post("", response_model=CertificationResponse, status_code=201)
def admin_create_certification(
    payload: CertificationCreate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return create_certification(db, payload.model_dump())


@router.patch("/{record_id}", response_model=CertificationResponse)
def admin_update_certification(
    record_id: UUID,
    payload: CertificationUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_certification_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Certification not found")

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    return update_certification(db, record, changes)


@router.delete("/{record_id}", status_code=204)
def admin_delete_certification(
    record_id: UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_certification_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Certification not found")

    delete_certification(db, record)
    return None