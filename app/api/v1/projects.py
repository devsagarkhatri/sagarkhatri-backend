
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.security.admin import require_admin
from app.services.project_service import (
    create_project,
    delete_project,
    get_all_projects,
    get_project,
    get_projects,
    update_project,
)
from app.services.chatbot.chatbot_cache import clear_chatbot_cache

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("", response_model=list[ProjectResponse])
def read_projects(db: Session = Depends(get_db)):
    """Public: return visible projects."""
    return get_projects(db)


@router.get("/admin", response_model=list[ProjectResponse])
def read_all_projects(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: return visible and hidden projects."""
    return get_all_projects(db)


@router.get("/admin/{project_id}", response_model=ProjectResponse)
def read_project_by_id(
    project_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: retrieve one project."""
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: create a project and its tags."""
    try:
        project = create_project(db, payload.model_dump())
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Project was created but could not be retrieved",
            )
        clear_chatbot_cache()
        return project
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A project with that slug may already exist",
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project",
        ) from exc


@router.patch("/{project_id}", response_model=ProjectResponse)
def edit_project(
    project_id: UUID,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: partially update a project."""
    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No project fields provided",
        )

    try:
        project = update_project(db, project_id, changes)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A project with that slug may already exist",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project",
        ) from exc

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    clear_chatbot_cache()
    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Admin: delete a project and its tags."""
    try:
        deleted = delete_project(db, project_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project",
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    clear_chatbot_cache()
    return None