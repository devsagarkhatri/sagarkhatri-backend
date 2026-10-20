
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SocialLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    platform: str
    url: str
    icon_url: str | None = None
    display_order: int
    visible: bool
    created_at: datetime
    updated_at: datetime


class SocialLinkCreate(BaseModel):
    platform: str
    url: str
    icon_url: str | None = None
    display_order: int = 0
    visible: bool = True


class SocialLinkUpdate(BaseModel):
    platform: str | None = None
    url: str | None = None
    icon_url: str | None = None
    display_order: int | None = None
    visible: bool | None = None