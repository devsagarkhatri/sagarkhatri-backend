
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.education import Education


def get_education(db: Session) -> list[Education]:
    result = db.execute(
        select(Education)
        .where(Education.visible.is_(True))
        .order_by(Education.display_order)
    )
    return list(result.scalars().all())


def get_all_education(db: Session) -> list[Education]:
    result = db.execute(
        select(Education).order_by(Education.display_order)
    )
    return list(result.scalars().all())


def get_education_by_id(db: Session, record_id: UUID) -> Education | None:
    return db.get(Education, record_id)


def create_education(db: Session, data: dict) -> Education:
    now = datetime.now(timezone.utc)
    record = Education(
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


def update_education(
    db: Session, record: Education, data: dict
) -> Education:
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


def delete_education(db: Session, record: Education) -> None:
    try:
        db.delete(record)
        db.commit()
    except Exception:
        db.rollback()
        raise