from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str | None
    headline: str | None

    hero_eyebrow: str | None
    hero_title_line_1: str | None
    hero_title_line_2: str | None
    hero_title_line_3: str | None
    hero_description: str | None

    about_eyebrow: str | None
    about_title: str | None
    about_description: str | None

    resume_url: str | None
    email: str | None
    location: str | None

    contact_eyebrow: str | None
    contact_title: str | None
    contact_mail_heading: str | None
    contact_social_heading: str | None

class ProfileUpdate(BaseModel):
    name: str | None = None
    headline: str | None = None

    hero_eyebrow: str | None = None
    hero_title_line_1: str | None = None
    hero_title_line_2: str | None = None
    hero_title_line_3: str | None = None
    hero_description: str | None = None

    about_eyebrow: str | None = None
    about_title: str | None = None
    about_description: str | None = None

    resume_url: str | None = None
    email: str | None = None
    location: str | None = None

    contact_eyebrow: str | None = None
    contact_title: str | None = None
    contact_mail_heading: str | None = None
    contact_social_heading: str | None = None