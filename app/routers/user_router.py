from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.db import get_db
from app.schemas.user_schema import (
    PasswordUpdate,
    UserCreate,
    UserResponse,
    UserUpdate
)
from app.services import user_service


# ==========================
# User Router
# ==========================

router = APIRouter(
    prefix="/users",
    tags=["USER"]
)


# ==========================
# Get Users
# ==========================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    user=Depends(get_current_user)
):
    return user


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    page: int = 1,
    page_size: int = 10,
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size

    return user_service.get_users(
        db,
        offset,
        page_size
    )


# ==========================
# Get User By ID
# ==========================

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    user = user_service.get_user(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ==========================
# Create User
# ==========================

@router.post(
    "",
    response_model=UserResponse
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    return user_service.create_user(
        db,
        user.name,
        user.password
    )


# ==========================
# Delete User
# ==========================

@router.delete(
    "/{user_id}",
    response_model=UserResponse
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    user = user_service.delete_user(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ==========================
# Update User
# ==========================

@router.put("/{user_id}/name", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    user = user_service.update_user(
        db,
        user_id,
        user_update
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ==========================
# Update Password
# ==========================

@router.put("/{user_id}/password", response_model=UserResponse)
def update_user_password(
    user_id: int,
    password: PasswordUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    user = user_service.update_user_password(
        db,
        user_id,
        password
    )

    if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    return user