
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.social_link import SocialLink


def get_social_links(db: Session) -> list[SocialLink]:
    result = db.execute(
        select(SocialLink)
        .where(SocialLink.visible.is_(True))
        .order_by(SocialLink.display_order)
    )
    return list(result.scalars().all())


def get_all_social_links(db: Session) -> list[SocialLink]:
    result = db.execute(
        select(SocialLink).order_by(SocialLink.display_order)
    )
    return list(result.scalars().all())


def get_social_link_by_id(
    db: Session, record_id: UUID
) -> SocialLink | None:
    return db.get(SocialLink, record_id)


def create_social_link(db: Session, data: dict) -> SocialLink:
    now = datetime.now(timezone.utc)
    record = SocialLink(
        id=uuid4(),
        created_at=now,
        updated_at=now,
        **data,
    )
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except Exception:
        db.rollback()
        raise


def update_social_link(
    db: Session, record: SocialLink, data: dict
) -> SocialLink:
    for field, value in data.items():
        setattr(record, field, value)

    record.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(record)
        return record
    except Exception:
        db.rollback()
        raise


def delete_social_link(db: Session, record: SocialLink) -> None:
    try:
        db.delete(record)
        db.commit()
    except Exception:
        db.rollback()
        raise