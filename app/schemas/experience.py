
from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ExperiencePointResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    content: str
    display_order: int


class ExperienceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    job_title: str
    company_name: str
    company_url: str | None
    company_logo_url: str | None
    location: str | None

    start_date: date | None
    end_date: date | None
    is_current: bool

    display_date: str | None
    icon_background: str | None

    display_order: int
    visible: bool
    points: list[ExperiencePointResponse]


class ExperiencePointInput(BaseModel):
    content: str = Field(min_length=1)
    display_order: int = Field(default=0, ge=0)


class ExperienceCreate(BaseModel):
    job_title: str = Field(min_length=1, max_length=255)
    company_name: str = Field(min_length=1, max_length=255)

    company_url: str | None = None
    company_logo_url: str | None = None
    location: str | None = Field(default=None, max_length=255)

    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False

    display_date: str | None = Field(default=None, max_length=255)
    icon_background: str | None = Field(default=None, max_length=255)

    display_order: int = Field(default=0, ge=0)
    visible: bool = True

    points: list[ExperiencePointInput] = Field(
        default_factory=list
    )


class ExperienceUpdate(BaseModel):
    job_title: str | None = Field(
        default=None, min_length=1, max_length=255
    )
    company_name: str | None = Field(
        default=None, min_length=1, max_length=255
    )

    company_url: str | None = None
    company_logo_url: str | None = None
    location: str | None = Field(default=None, max_length=255)

    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None

    display_date: str | None = Field(default=None, max_length=255)
    icon_background: str | None = Field(default=None, max_length=255)

    display_order: int | None = Field(default=None, ge=0)
    visible: bool | None = None

    points: list[ExperiencePointInput] | None = None