from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class TechnologyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    icon_url: str | None
    category: str | None
    display_order: int
    visible: bool

class TechnologyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    icon_url: str | None = None
    category: str | None = Field(default=None, max_length=100)
    display_order: int = Field(default=0, ge=0)
    visible: bool = True

class TechnologyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    icon_url: str | None = None
    category: str | None = Field(default=None, max_length=100)
    display_order: int | None = Field(default=None, ge=0)
    visible: bool | None = None
