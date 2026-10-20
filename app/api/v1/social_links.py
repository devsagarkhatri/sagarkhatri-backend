
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security.admin import require_admin
from app.schemas.social_link import (
    SocialLinkCreate,
    SocialLinkResponse,
    SocialLinkUpdate,
)
from app.services.social_link_service import (
    get_social_links,
    get_all_social_links,
    get_social_link_by_id,
    create_social_link,
    update_social_link,
    delete_social_link,
)

router = APIRouter(prefix="/social-links", tags=["Social Links"])


@router.get("", response_model=list[SocialLinkResponse])
def list_social_links(db: Session = Depends(get_db)):
    return get_social_links(db)


@router.get("/admin", response_model=list[SocialLinkResponse])
def admin_list_social_links(
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return get_all_social_links(db)


@router.get("/admin/{record_id}", response_model=SocialLinkResponse)
def admin_get_social_link(
    record_id: UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_social_link_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Social link not found")
    return record


@router.post("", response_model=SocialLinkResponse, status_code=201)
def admin_create_social_link(
    payload: SocialLinkCreate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return create_social_link(db, payload.model_dump())


@router.patch("/{record_id}", response_model=SocialLinkResponse)
def admin_update_social_link(
    record_id: UUID,
    payload: SocialLinkUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_social_link_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Social link not found")

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    return update_social_link(db, record, changes)


@router.delete("/{record_id}", status_code=204)
def admin_delete_social_link(
    record_id: UUID,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    record = get_social_link_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Social link not found")

    delete_social_link(db, record)
    return None