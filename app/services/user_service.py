from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.repositories import user_repo
from app.schemas.user_schema import (
    PasswordUpdate,
    UserUpdate
)


# ==========================
# Get Users
# ==========================

def get_users(
    db: Session,
    offset: int,
    limit: int
):
    return user_repo.get_all(
        db,
        offset,
        limit
    )


def get_user(
    db: Session,
    user_id: int
):
    return user_repo.get_by_id(
        db,
        user_id
    )


# ==========================
# Create User
# ==========================

def create_user(
    db: Session,
    name: str,
    password: str
):
    hashed_password = hash_password(
        password
    )

    return user_repo.create(
        db,
        name,
        hashed_password
    )


# ==========================
# Delete User
# ==========================

def delete_user(
    db: Session,
    user_id: int
):
    return user_repo.delete(
        db,
        user_id
    )


# ==========================
# Update User
# ==========================

def update_user(
    db: Session,
    user_id: int,
    user_update: UserUpdate
):
    return user_repo.update(
        db,
        user_id,
        user_update.name
    )


# ==========================
# Update Password
# ==========================

def update_user_password(
    db: Session,
    user_id: int,
    passwords: PasswordUpdate
):
    user = user_repo.get_by_id(
        db,
        user_id
    )

    if not user:
        return None


    if not verify_password(
        passwords.old_password,
        user.hashed_password
    ):
        return None


    hashed_password = hash_password(
        passwords.new_password
    )


    return user_repo.update_password(
        db,
        user_id,
        hashed_password
    )