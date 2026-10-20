from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.profile import Profile


def get_profile(db: Session) -> Profile | None:
    statement = select(Profile).limit(1)
    result = db.execute(statement)
    return result.scalar_one_or_none()


def update_profile(
    db: Session,
    changes: dict,
) -> Profile | None:
    profile = get_profile(db)

    if profile is None:
        return None

    for field, value in changes.items():
        setattr(profile, field, value)

    profile.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(profile)
    except Exception:
        db.rollback()
        raise

    return profile