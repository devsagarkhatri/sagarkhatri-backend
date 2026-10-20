from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    name: Mapped[str | None] = mapped_column(String(255))
    headline: Mapped[str | None] = mapped_column(String(255))

    hero_eyebrow: Mapped[str | None] = mapped_column(String(255))
    hero_title_line_1: Mapped[str | None] = mapped_column(String(255))
    hero_title_line_2: Mapped[str | None] = mapped_column(String(255))
    hero_title_line_3: Mapped[str | None] = mapped_column(String(255))
    hero_description: Mapped[str | None] = mapped_column(Text)

    about_eyebrow: Mapped[str | None] = mapped_column(String(255))
    about_title: Mapped[str | None] = mapped_column(String(255))
    about_description: Mapped[str | None] = mapped_column(Text)

    resume_url: Mapped[str | None] = mapped_column(Text)
    email: Mapped[str | None] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(255))

    contact_eyebrow: Mapped[str | None] = mapped_column(String(255))
    contact_title: Mapped[str | None] = mapped_column(String(255))
    contact_mail_heading: Mapped[str | None] = mapped_column(String(255))
    contact_social_heading: Mapped[str | None] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))