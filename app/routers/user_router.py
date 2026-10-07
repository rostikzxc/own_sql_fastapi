from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from pydantic import TypeAdapter

from app.dependencies.redis import get_redis
from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.db import get_db
from app.models.user import User
from app.schemas.user_schema import (
    PasswordUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["USER"])


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user


@router.get("", response_model=list[UserResponse])
async def get_users(  
    page: int = 1,
    page_size: int = 10,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    offset = (page - 1) * page_size
    cache_key = f"users:page:{page}:size:{page_size}"

    cached_users = await redis.get(cache_key)
    if cached_users:
        return TypeAdapter(list[UserResponse]).validate_json(cached_users)

    users = UserService(db).get_users(offset, page_size)
    users_response = [UserResponse.model_validate(user) for user in users]

    await redis.set(
        cache_key,
        TypeAdapter(list[UserResponse]).dump_json(users_response),
        ex=60,
    )
    return users_response


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    redis: Redis = Depends(get_redis),
):
    cache_key = f"user:{user_id}"
    cached_user = await redis.get(cache_key)

    if cached_user:
        return UserResponse.model_validate_json(cached_user)

    user = UserService(db).get_user(user_id)
    user_response = UserResponse.model_validate(user)

    await redis.set(cache_key, user_response.model_dump_json(), ex=60)
    return user_response


@router.post("", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return UserService(db).create_user(user.name, user.password)


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    redis: Redis = Depends(get_redis),
):
    user = UserService(db).delete_user(user_id)

    await redis.delete(f"user:{user_id}")
    async for key in redis.scan_iter(match="users:page*"):
        await redis.delete(key)

    return user


@router.put("/{user_id}/name", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    redis: Redis = Depends(get_redis),
):
    user = UserService(db).update_user(user_id, user_update)

    await redis.delete(f"user:{user_id}")
    async for key in redis.scan_iter(match="users:page*"):
        await redis.delete(key)

    return user


@router.put("/{user_id}/password", response_model=UserResponse)
def update_user_password(
    user_id: int,
    password: PasswordUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return UserService(db).update_user_password(user_id, password)