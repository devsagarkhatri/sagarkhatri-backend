
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service import Service


def get_services(db: Session) -> list[Service]:
    result = db.execute(
        select(Service)
        .where(Service.visible.is_(True))
        .order_by(Service.display_order)
    )
    return list(result.scalars().all())


def get_all_services(db: Session) -> list[Service]:
    result = db.execute(select(Service).order_by(Service.display_order))
    return list(result.scalars().all())


def get_service_by_id(db: Session, record_id: UUID) -> Service | None:
    return db.get(Service, record_id)


def create_service(db: Session, data: dict) -> Service:
    now = datetime.now(timezone.utc)
    record = Service(
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


def update_service(
    db: Session, record: Service, data: dict
) -> Service:
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


def delete_service(db: Session, record: Service) -> None:
    try:
        db.delete(record)
        db.commit()
    except Exception:
        db.rollback()
        raise