
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.certification import Certification


def get_certifications(db: Session) -> list[Certification]:
    result = db.execute(
        select(Certification)
        .where(Certification.visible.is_(True))
        .order_by(Certification.display_order)
    )
    return list(result.scalars().all())


def get_all_certifications(db: Session) -> list[Certification]:
    result = db.execute(
        select(Certification).order_by(Certification.display_order)
    )
    return list(result.scalars().all())


def get_certification_by_id(
    db: Session, record_id: UUID
) -> Certification | None:
    return db.get(Certification, record_id)


def create_certification(db: Session, data: dict) -> Certification:
    now = datetime.now(timezone.utc)
    record = Certification(
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


def update_certification(
    db: Session, record: Certification, data: dict
) -> Certification:
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


def delete_certification(db: Session, record: Certification) -> None:
    try:
        db.delete(record)
        db.commit()
    except Exception:
        db.rollback()
        raise