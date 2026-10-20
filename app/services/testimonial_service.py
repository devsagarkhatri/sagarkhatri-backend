
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.testimonial import Testimonial


def get_testimonials(db: Session) -> list[Testimonial]:
    result = db.execute(
        select(Testimonial)
        .where(Testimonial.visible.is_(True))
        .order_by(Testimonial.display_order)
    )
    return list(result.scalars().all())


def get_all_testimonials(db: Session) -> list[Testimonial]:
    result = db.execute(
        select(Testimonial).order_by(Testimonial.display_order)
    )
    return list(result.scalars().all())


def get_testimonial_by_id(
    db: Session, record_id: UUID
) -> Testimonial | None:
    return db.get(Testimonial, record_id)


def create_testimonial(db: Session, data: dict) -> Testimonial:
    now = datetime.now(timezone.utc)
    record = Testimonial(
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


def update_testimonial(
    db: Session, record: Testimonial, data: dict
) -> Testimonial:
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


def delete_testimonial(db: Session, record: Testimonial) -> None:
    try:
        db.delete(record)
        db.commit()
    except Exception:
        db.rollback()
        raise