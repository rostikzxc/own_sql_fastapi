from datetime import datetime, timedelta, timezone

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
from app.repositories import refresh_token_repo
from app.repositories.user_repo import (
    create,
    get_by_name,
)


# ==========================
# Register
# ==========================

def register(
    db: Session,
    name: str,
    password: str
):
    user = get_by_name(
        db,
        name
    )

    if user:
        return None

    hashed_password = hash_password(
        password
    )

    return create(
        db,
        name,
        hashed_password
    )


# ==========================
# Login
# ==========================

def login(
    db: Session,
    name: str,
    password: str
):
    user = get_by_name(
        db,
        name
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None


    access_token = create_access_token({
        "user_id": user.id
    })

    refresh_token = create_refresh_token({
        "user_id": user.id
    })


    token_hash = hash_refresh_token(
        refresh_token
    )


    expires_at = datetime.now(
        timezone.utc
    ) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )


    refresh_token_repo.create(
        db,
        user.id,
        token_hash,
        expires_at
    )


    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


# ==========================
# Refresh Token
# ==========================

def refresh_token(
    db: Session,
    refresh_token: str
):
    payload = decode_token(
        refresh_token
    )

    if not payload:
        return None


    if payload.get("type") != "refresh":
        return None


    token_hash = hash_refresh_token(
        refresh_token
    )


    stored_token = refresh_token_repo.get_by_hash(
        db,
        token_hash
    )


    if not stored_token:
        return None


    if stored_token.revoked:
        return None


    if stored_token.expires_at < datetime.now():
        return None


    user_id = payload.get(
        "user_id"
    )


    access_token = create_access_token({
        "user_id": user_id
    })


    return {
        "access_token": access_token
    }


# ==========================
# Logout
# ==========================

def logout(
    db: Session,
    refresh_token: str
):
    token_hash = hash_refresh_token(
        refresh_token
    )

    return refresh_token_repo.revoke(
        db,
        token_hash
    )