
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectTagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    display_order: int


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str

    description: str | None
    long_description: str | None

    image_url: str | None
    github_url: str | None
    live_url: str | None

    featured: bool
    visible: bool
    display_order: int

    tags: list[ProjectTagResponse]


class ProjectTagInput(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    display_order: int = Field(default=0, ge=0)


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)

    description: str | None = None
    long_description: str | None = None

    image_url: str | None = None
    github_url: str | None = None
    live_url: str | None = None

    featured: bool = False
    visible: bool = True
    display_order: int = Field(default=0, ge=0)

    tags: list[ProjectTagInput] = Field(default_factory=list)


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None, min_length=1, max_length=255
    )
    slug: str | None = Field(
        default=None, min_length=1, max_length=255
    )

    description: str | None = None
    long_description: str | None = None

    image_url: str | None = None
    github_url: str | None = None
    live_url: str | None = None

    featured: bool | None = None
    visible: bool | None = None
    display_order: int | None = Field(default=None, ge=0)

    tags: list[ProjectTagInput] | None = None