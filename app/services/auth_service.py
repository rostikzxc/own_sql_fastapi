from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.repositories.refresh_token_repo import RefreshTokenRepository
from app.repositories.user_repo import UserRepository


class AuthService:

    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.tokens = RefreshTokenRepository(db)

    def register(self, name: str, password: str):
        if self.users.get_by_name(name) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this name already exists",
            )

        hashed_password = hash_password(password)
        return self.users.create(name, hashed_password)

    def login(self, name: str, password: str) -> dict:
        user = self.users.get_by_name(name)

        invalid_credentials = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid name or password",
        )

        if user is None:
            raise invalid_credentials
        if not verify_password(password, user.hashed_password):
            raise invalid_credentials

        access_token = create_access_token({"user_id": user.id})
        refresh_token = create_refresh_token({"user_id": user.id})

        token_hash = hash_refresh_token(refresh_token)
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        self.tokens.create(user.id, token_hash, expires_at)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh_access_token(self, refresh_token: str) -> dict:
        invalid_token = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

        payload = decode_token(refresh_token)
        if payload is None or payload.get("type") != "refresh":
            raise invalid_token

        token_hash = hash_refresh_token(refresh_token)
        stored_token = self.tokens.get_by_hash(token_hash)

        if stored_token is None or stored_token.revoked:
            raise invalid_token
        if stored_token.expires_at < datetime.now(timezone.utc):
            raise invalid_token

        user_id = payload.get("user_id")
        access_token = create_access_token({"user_id": user_id})
        return {"access_token": access_token}

    def logout(self, refresh_token: str) -> None:
        token_hash = hash_refresh_token(refresh_token)
        stored_token = self.tokens.get_by_hash(token_hash)

        if stored_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        self.tokens.revoke(stored_token)

        