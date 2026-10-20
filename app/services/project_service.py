
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.project import Project
from app.models.project_tag import ProjectTag


def get_projects(db: Session) -> list[Project]:
    """Return visible projects for the public portfolio."""
    statement = (
        select(Project)
        .options(selectinload(Project.tags))
        .where(Project.visible.is_(True))
        .order_by(Project.display_order)
    )
    result = db.execute(statement)
    return list(result.scalars().all())


def get_project(db: Session, project_id: UUID) -> Project | None:
    """Return one project, including hidden projects."""
    statement = (
        select(Project)
        .options(selectinload(Project.tags))
        .where(Project.id == project_id)
    )
    return db.execute(statement).scalar_one_or_none()


def get_all_projects(db: Session) -> list[Project]:
    """Return all projects for authorized administration."""
    statement = (
        select(Project)
        .options(selectinload(Project.tags))
        .order_by(Project.display_order)
    )
    result = db.execute(statement)
    return list(result.scalars().all())


def create_project(db: Session, data: dict) -> Project:
    """Create a project and its tags in one transaction."""
    now = datetime.now(timezone.utc)
    values = dict(data)
    tag_data = values.pop("tags", [])

    project = Project(
        id=uuid4(),
        **values,
        created_at=now,
        updated_at=now,
    )

    for item in tag_data:
        project.tags.append(
            ProjectTag(
                id=uuid4(),
                name=item["name"],
                display_order=item.get("display_order", 0),
            )
        )

    try:
        db.add(project)
        db.commit()
        return get_project(db, project.id)
    except Exception:
        db.rollback()
        raise


def update_project(
    db: Session,
    project_id: UUID,
    changes: dict,
) -> Project | None:
    """Partially update a project and optionally replace its tags."""
    project = get_project(db, project_id)
    if project is None:
        return None

    values = dict(changes)
    tag_data = values.pop("tags", None)

    for field in ("name", "slug"):
        if field in values and values[field] is None:
            raise ValueError(f"{field} cannot be null")

    now = datetime.now(timezone.utc)

    try:
        for field, value in values.items():
            setattr(project, field, value)

        if tag_data is not None:
            project.tags.clear()

            for item in tag_data:
                project.tags.append(
                    ProjectTag(
                        id=uuid4(),
                        name=item["name"],
                        display_order=item.get("display_order", 0),
                    )
                )

        project.updated_at = now
        db.commit()
        return get_project(db, project_id)

    except Exception:
        db.rollback()
        raise


def delete_project(db: Session, project_id: UUID) -> bool:
    """Delete a project and its related tags."""
    project = get_project(db, project_id)
    if project is None:
        return False

    try:
        db.delete(project)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise