from fastapi import APIRouter, Depends

from app.models.admin_user import AdminUser
from app.security.admin import require_admin


router = APIRouter(
    prefix="/security-test",
    tags=["Security Test1"],
)


@router.get("/admin")
def admin_security_test(
    admin: AdminUser = Depends(require_admin),
):
    return {
        "authorized": True,
        "role": admin.role,
        "is_active": admin.is_active,
    }
