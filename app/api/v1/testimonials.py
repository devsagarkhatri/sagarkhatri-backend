
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security.admin import require_admin
from app.schemas.testimonial import (
    TestimonialCreate,
    TestimonialResponse,
    TestimonialUpdate,
)
from app.services.testimonial_service import (
    get_testimonials,
    get_all_testimonials,
    get_testimonial_by_id,
    create_testimonial,
    update_testimonial,
    delete_testimonial,
)

router = APIRouter(prefix="/testimonials", tags=["Testimonials"])


@router.get("", response_model=list[TestimonialResponse])
def list_testimonials(db: Session = Depends(get_db)):
    return get_testimonials(db)


@router.get("/admin", response_model=list[TestimonialResponse])
def admin_list_testimonials(
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return get_all_testimonials(db)


@router.get("/admin/{record_id}", response_model=TestimonialResponse)
def admin_get_testimonial(
    record_id: UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_testimonial_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return record


@router.post("", response_model=TestimonialResponse, status_code=201)
def admin_create_testimonial(
    payload: TestimonialCreate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return create_testimonial(db, payload.model_dump())


@router.patch("/{record_id}", response_model=TestimonialResponse)
def admin_update_testimonial(
    record_id: UUID,
    payload: TestimonialUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_testimonial_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    return update_testimonial(db, record, changes)


@router.delete("/{record_id}", status_code=204)
def admin_delete_testimonial(
    record_id: UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_testimonial_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    delete_testimonial(db, record)
    return None