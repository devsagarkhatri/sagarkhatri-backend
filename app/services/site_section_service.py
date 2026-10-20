from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.site_section import SiteSection


def get_site_sections(db: Session) -> list[SiteSection]:
    """Return visible site sections for the public portfolio."""
    statement = (
        select(SiteSection)
        .where(SiteSection.visible.is_(True))
        .order_by(SiteSection.display_order)
    )
    return list(db.execute(statement).scalars().all())


def get_all_site_sections(db: Session) -> list[SiteSection]:
    """Return all records for authorized administration."""
    statement = select(SiteSection).order_by(SiteSection.display_order)
    return list(db.execute(statement).scalars().all())


def get_site_section(db: Session, record_id: UUID) -> SiteSection | None:
    """Retrieve one record, including hidden records."""
    statement = select(SiteSection).where(SiteSection.id == record_id)
    return db.execute(statement).scalar_one_or_none()


def create_site_section(db: Session, data: dict) -> SiteSection:
    """Create a record in a transaction."""
    now = datetime.now(timezone.utc)
    record = SiteSection(id=uuid4(), **data, created_at=now, updated_at=now)
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except Exception:
        db.rollback()
        raise


def update_site_section(db: Session, record_id: UUID, changes: dict) -> SiteSection | None:
    """Partially update a record in a transaction."""
    record = get_site_section(db, record_id)
    if record is None:
        return None

    values = dict(changes)
    for field in ['key']:
        if field in values and values[field] is None:
            raise ValueError(f"{field} cannot be null")

    try:
        for field, value in values.items():
            setattr(record, field, value)
        record.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(record)
        return record
    except Exception:
        db.rollback()
        raise


def delete_site_section(db: Session, record_id: UUID) -> bool:
    """Delete a record in a transaction."""
    record = get_site_section(db, record_id)
    if record is None:
        return False
    try:
        db.delete(record)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
