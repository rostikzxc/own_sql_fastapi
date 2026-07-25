from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.dependencies.db import get_db
from app.repositories import user_repo


# ==========================
# Authentication
# ==========================

oauth2_schema = HTTPBearer()


def get_current_user(
    credentials=Depends(oauth2_schema),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = decode_token(token)

    if not payload:
        return None

    if payload.get("type") != "access":
        return None

    user_id = payload.get("user_id")

    if not user_id:
        return None

    return user_repo.get_by_id(
        db,
        user_id
    )


# ==========================
# Authorization
# ==========================

def require_admin(
    user=Depends(get_current_user)
):
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not Authenticated"
        )

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="User Not Admin"
        )

    return user