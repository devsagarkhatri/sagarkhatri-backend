
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TestimonialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    testimonial: str
    person_name: str
    designation: str | None = None
    company: str | None = None
    profile_image_url: str | None = None
    company_url: str | None = None
    display_order: int
    visible: bool
    created_at: datetime
    updated_at: datetime


class TestimonialCreate(BaseModel):
    testimonial: str
    person_name: str
    designation: str | None = None
    company: str | None = None
    profile_image_url: str | None = None
    company_url: str | None = None
    display_order: int = 0
    visible: bool = True


class TestimonialUpdate(BaseModel):
    testimonial: str | None = None
    person_name: str | None = None
    designation: str | None = None
    company: str | None = None
    profile_image_url: str | None = None
    company_url: str | None = None
    display_order: int | None = None
    visible: bool | None = None