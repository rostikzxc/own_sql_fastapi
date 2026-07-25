from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.auth_schema import (
    LoginSchema,
    RegisterSchema,
    RefreshTokenSchema,
    TokenResponse
)
from app.services import auth_service


# ==========================
# Auth Router
# ==========================

router = APIRouter(
    prefix="/auth",
    tags=["AUTH"]
)


# ==========================
# Register
# ==========================

@router.post("/register")
def register(
    user: RegisterSchema,
    db: Session = Depends(get_db)
):
    return auth_service.register(
        db,
        user.name,
        user.password
    )


# ==========================
# Login
# ==========================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user: LoginSchema,
    db: Session = Depends(get_db)
):
    tokens = auth_service.login(
        db,
        user.name,
        user.password
    )

    if not tokens:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return tokens


# ==========================
# Refresh Token
# ==========================

@router.post("/refresh")
def refresh_token(
    data: RefreshTokenSchema,
    db: Session = Depends(get_db)
):
    return auth_service.refresh_token(
        db,
        data.refresh_token
    )


# ==========================
# Logout
# ==========================

@router.post("/logout")
def logout(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    return auth_service.logout(
        db,
        refresh_token
    )