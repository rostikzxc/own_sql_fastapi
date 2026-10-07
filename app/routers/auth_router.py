from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.dependencies.redis import get_redis
from app.dependencies.db import get_db
from app.schemas.auth_schema import (
    LoginSchema,
    RegisterSchema,
    RefreshTokenSchema,
    TokenResponse,
)
from app.schemas.user_schema import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["AUTH"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user: RegisterSchema,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    new_user = AuthService(db).register(user.name, user.password)

    async for key in redis.scan_iter(match="users:page:*"):
        await redis.delete(key)

    return new_user


@router.post("/login", response_model=TokenResponse)
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
        raise HTTPException(status_code=429, detail="Too many requests")

    return AuthService(db).login(user.name, user.password)


@router.post("/refresh")
def refresh_token(data: RefreshTokenSchema, db: Session = Depends(get_db)):
    return AuthService(db).refresh_access_token(data.refresh_token)


@router.post("/logout", status_code=204)
def logout(data: RefreshTokenSchema, db: Session = Depends(get_db)):
    AuthService(db).logout(data.refresh_token)