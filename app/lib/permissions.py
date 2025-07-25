from fastapi import Depends, HTTPException, status
from app.infra.db.models.users import User as UserModel
from .oauth2 import get_current_user


async def get_current_active_superuser(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a superuser"
        )
    return current_user
