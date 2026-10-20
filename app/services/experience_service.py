
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.experience import Experience
from app.models.experience_point import ExperiencePoint


def get_experiences(db: Session) -> list[Experience]:
    """Return visible experiences for the public portfolio."""
    statement = (
        select(Experience)
        .options(selectinload(Experience.points))
        .where(Experience.visible.is_(True))
        .order_by(Experience.display_order)
    )

    result = db.execute(statement)
    return list(result.scalars().all())


def get_experience(
    db: Session,
    experience_id: UUID,
) -> Experience | None:
    """Return one experience, including hidden records."""
    statement = (
        select(Experience)
        .options(selectinload(Experience.points))
        .where(Experience.id == experience_id)
    )

    return db.execute(statement).scalar_one_or_none()


def get_all_experiences(db: Session) -> list[Experience]:
    """Return all experiences for authorized administration."""
    statement = (
        select(Experience)
        .options(selectinload(Experience.points))
        .order_by(Experience.display_order)
    )

    result = db.execute(statement)
    return list(result.scalars().all())


def create_experience(
    db: Session,
    data: dict,
) -> Experience:
    """Create an experience and its points in one transaction."""
    now = datetime.now(timezone.utc)
    values = dict(data)
    point_data = values.pop("points", [])

    experience = Experience(
        id=uuid4(),
        **values,
        created_at=now,
        updated_at=now,
    )

    for item in point_data:
        experience.points.append(
            ExperiencePoint(
                id=uuid4(),
                content=item["content"],
                display_order=item.get("display_order", 0),
                created_at=now,
                updated_at=now,
            )
        )

    try:
        db.add(experience)
        db.commit()
        db.refresh(experience)

        # Load the relationship while the session is active.
        _ = experience.points

        return experience
    except Exception:
        db.rollback()
        raise


def update_experience(
    db: Session,
    experience_id: UUID,
    changes: dict,
) -> Experience | None:
    """Partially update an experience and optionally replace its points."""
    experience = get_experience(db, experience_id)

    if experience is None:
        return None

    values = dict(changes)
    point_data = values.pop("points", None)

    # These database columns are non-nullable.
    for field in ("job_title", "company_name"):
        if field in values and values[field] is None:
            raise ValueError(f"{field} cannot be null")

    now = datetime.now(timezone.utc)

    try:
        for field, value in values.items():
            setattr(experience, field, value)

        if point_data is not None:
            # Relationship cascade deletes the replaced point records.
            experience.points.clear()

            for item in point_data:
                experience.points.append(
                    ExperiencePoint(
                        id=uuid4(),
                        content=item["content"],
                        display_order=item.get("display_order", 0),
                        created_at=now,
                        updated_at=now,
                    )
                )

        experience.updated_at = now

        db.commit()

        # Re-query with the relationship loaded after commit.
        updated = get_experience(db, experience_id)
        return updated

    except Exception:
        db.rollback()
        raise


def delete_experience(
    db: Session,
    experience_id: UUID,
) -> bool:
    """Delete an experience and its related points."""
    experience = get_experience(db, experience_id)

    if experience is None:
        return False

    try:
        db.delete(experience)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise