from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.technology import Technology


def get_technologies(db: Session) -> list[Technology]:
    """Return visible technologies for the public portfolio."""
    statement = (
        select(Technology)
        .where(Technology.visible.is_(True))
        .order_by(Technology.display_order)
    )
    return list(db.execute(statement).scalars().all())


def get_all_technologies(db: Session) -> list[Technology]:
    """Return all records for authorized administration."""
    statement = select(Technology).order_by(Technology.display_order)
    return list(db.execute(statement).scalars().all())


def get_technology(db: Session, record_id: UUID) -> Technology | None:
    """Retrieve one record, including hidden records."""
    statement = select(Technology).where(Technology.id == record_id)
    return db.execute(statement).scalar_one_or_none()


def create_technology(db: Session, data: dict) -> Technology:
    """Create a record in a transaction."""
    now = datetime.now(timezone.utc)
    record = Technology(id=uuid4(), **data, created_at=now, updated_at=now)
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except Exception:
        db.rollback()
        raise


def update_technology(db: Session, record_id: UUID, changes: dict) -> Technology | None:
    """Partially update a record in a transaction."""
    record = get_technology(db, record_id)
    if record is None:
        return None

    values = dict(changes)
    for field in ['name']:
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


def delete_technology(db: Session, record_id: UUID) -> bool:
    """Delete a record in a transaction."""
    record = get_technology(db, record_id)
    if record is None:
        return False
    try:
        db.delete(record)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
