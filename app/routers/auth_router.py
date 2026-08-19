from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.dependencies.redis import get_redis
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
async def register(
    user: RegisterSchema,
    request: Request,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)
):

    new_user = auth_service.register(
        db,
        user.name,
        user.password
    )

    async for key in redis.scan_iter(match="users:page:*"):
            await redis.delete(key)

    return new_user


# ==========================
# Login
# ==========================

@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    user: LoginSchema,
    request: Request,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):

    ip = request.client.host

    ip_key = f"rate_limit:login:{ip}"
    name_key = f"rate_limit:login:{user.name}"
    
    ip_attempts = await redis.incr(ip_key)
    name_attempts = await redis.incr(name_key)

    if ip_attempts == 1:
        await redis.expire(ip_key, 60)

    if name_attempts == 1:
        await redis.expire(name_key, 60)

    if ip_attempts > 5 or name_attempts > 5:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )

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