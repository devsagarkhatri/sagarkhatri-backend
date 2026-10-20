from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class SiteSectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    key: str
    title: str | None
    nav_title: str | None
    visible: bool
    display_order: int

class SiteSectionCreate(BaseModel):
    key: str = Field(min_length=1, max_length=100)
    title: str | None = Field(default=None, max_length=255)
    nav_title: str | None = Field(default=None, max_length=255)
    visible: bool = True
    display_order: int = Field(default=0, ge=0)

class SiteSectionUpdate(BaseModel):
    key: str | None = Field(default=None, min_length=1, max_length=100)
    title: str | None = Field(default=None, max_length=255)
    nav_title: str | None = Field(default=None, max_length=255)
    visible: bool | None = None
    display_order: int | None = Field(default=None, ge=0)
