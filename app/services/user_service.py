from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import PasswordUpdate, UserUpdate


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def get_users(self, offset: int, limit: int) -> list[User]:
        return self.repo.get_all(offset, limit)

    def get_user(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def create_user(self, name: str, password: str) -> User:
        hashed_password = hash_password(password)
        return self.repo.create(name, hashed_password)

    def delete_user(self, user_id: int) -> User:
    user = self.get_user(user_id)
    self.repo.delete(user)
    return user

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.get_user(user_id)
        return self.repo.update(user, user_update.name)

    def update_user_password(self, user_id: int, passwords: PasswordUpdate) -> User:
        user = self.get_user(user_id)

        if not verify_password(passwords.old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect",
            )

        hashed_password = hash_password(passwords.new_password)
        return self.repo.update_password(user, hashed_password)