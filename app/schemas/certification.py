
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CertificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    issuer: str
    issue_date: date | None = None
    credential_id: str | None = None
    credential_url: str | None = None
    certificate_url: str | None = None
    description: str | None = None
    logo_url: str | None = None
    display_order: int
    visible: bool
    created_at: datetime
    updated_at: datetime


class CertificationCreate(BaseModel):
    name: str
    issuer: str
    issue_date: date | None = None
    credential_id: str | None = None
    credential_url: str | None = None
    certificate_url: str | None = None
    description: str | None = None
    logo_url: str | None = None
    display_order: int = 0
    visible: bool = True


class CertificationUpdate(BaseModel):
    name: str | None = None
    issuer: str | None = None
    issue_date: date | None = None
    credential_id: str | None = None
    credential_url: str | None = None
    certificate_url: str | None = None
    description: str | None = None
    logo_url: str | None = None
    display_order: int | None = None
    visible: bool | None = None