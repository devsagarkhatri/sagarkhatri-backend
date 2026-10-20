
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EducationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    degree: str
    institution: str
    institution_url: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    display_period: str | None = None
    description: str | None = None
    logo_url: str | None = None
    display_order: int
    visible: bool
    created_at: datetime
    updated_at: datetime


class EducationCreate(BaseModel):
    degree: str
    institution: str
    institution_url: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    display_period: str | None = None
    description: str | None = None
    logo_url: str | None = None
    display_order: int = 0
    visible: bool = True


class EducationUpdate(BaseModel):
    degree: str | None = None
    institution: str | None = None
    institution_url: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    display_period: str | None = None
    description: str | None = None
    logo_url: str | None = None
    display_order: int | None = None
    visible: bool | None = None