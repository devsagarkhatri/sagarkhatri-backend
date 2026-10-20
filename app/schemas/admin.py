from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AdminMeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    authorized: bool
    admin_id: UUID
    supabase_user_id: UUID
    email: str
    role: str
    is_active: bool