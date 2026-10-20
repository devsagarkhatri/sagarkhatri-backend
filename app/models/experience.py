from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    company_url: Mapped[str | None] = mapped_column(Text)
    company_logo_url: Mapped[str | None] = mapped_column(Text)

    location: Mapped[str | None] = mapped_column(String(255))

    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)

    display_date: Mapped[str | None] = mapped_column(String(255))
    icon_background: Mapped[str | None] = mapped_column(String(255))

    display_order: Mapped[int] = mapped_column(Integer, default=0)
    visible: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    points: Mapped[list["ExperiencePoint"]] = relationship(
        back_populates="experience",
        cascade="all, delete-orphan",
        order_by="ExperiencePoint.display_order",
    )