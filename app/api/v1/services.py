
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security.admin import require_admin
from app.schemas.service import (
    ServiceCreate,
    ServiceResponse,
    ServiceUpdate,
)
from app.services.service_service import (
    get_services,
    get_all_services,
    get_service_by_id,
    create_service,
    update_service,
    delete_service,
)

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("", response_model=list[ServiceResponse])
def list_services(db: Session = Depends(get_db)):
    return get_services(db)


@router.get("/admin", response_model=list[ServiceResponse])
def admin_list_services(
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return get_all_services(db)


@router.get("/admin/{record_id}", response_model=ServiceResponse)
def admin_get_service(
    record_id: UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_service_by_id(db, record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    return record


@router.post("", response_model=ServiceResponse, status_code=201)
def admin_create_service(
    payload: ServiceCreate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return create_service(db, payload.model_dump())


@router.patch("/{record_id}", response_model=ServiceResponse)
def admin_update_service(
    record_id: UUID,
    payload: ServiceUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_service_by_id(db, record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="No fields provided to update",
        )

    return update_service(db, record, changes)


@router.delete("/{record_id}", status_code=204)
def admin_delete_service(
    record_id: UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_service_by_id(db, record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    delete_service(db, record)
    return None
