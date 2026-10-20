from fastapi import APIRouter, Depends

from app.models.admin_user import AdminUser
from app.schemas.admin import AdminMeResponse
from app.security.admin import require_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/me", response_model=AdminMeResponse)
def read_admin_me(
    admin_user: AdminUser = Depends(require_admin),
):
    return {
        "authorized": True,
        "admin_id": admin_user.id,
        "supabase_user_id": admin_user.supabase_user_id,
        "email": admin_user.email,
        "role": admin_user.role,
        "is_active": admin_user.is_active,
    }