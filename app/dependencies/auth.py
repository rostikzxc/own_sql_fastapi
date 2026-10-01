from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.dependencies.db import get_db
from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository


oauth2_schema = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_schema),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    payload = decode_token(credentials.credentials)
    if payload is None:
        raise unauthorized

    if payload.get("type") != "access":
        raise unauthorized

    user_id = payload.get("user_id")
    if user_id is None:
        raise unauthorized

    user = UserRepository(db).get_by_id(user_id)
    if user is None:
        raise unauthorized

    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin",
        )
    return user