from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.admin_user import AdminUser
from app.security.supabase_auth import require_aal2


def require_admin(
    claims: dict = Depends(require_aal2),
    db: Session = Depends(get_db),
) -> AdminUser:
    user_id = claims.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User identity missing from token",
        )

    try:
        supabase_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identity",
        )

    statement = select(AdminUser).where(
        AdminUser.supabase_user_id == supabase_user_id,
        AdminUser.is_active.is_(True),
    )

    admin_user = db.execute(statement).scalar_one_or_none()

    if admin_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return admin_user