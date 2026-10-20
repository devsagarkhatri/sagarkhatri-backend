from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Testimonial(Base):
    __tablename__ = "testimonials"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    testimonial: Mapped[str] = mapped_column(Text, nullable=False)

    person_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    designation: Mapped[str | None] = mapped_column(String(255))
    company: Mapped[str | None] = mapped_column(String(255))
    profile_image_url: Mapped[str | None] = mapped_column(Text)
    company_url: Mapped[str | None] = mapped_column(Text)

    display_order: Mapped[int] = mapped_column(Integer, default=0)
    visible: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))