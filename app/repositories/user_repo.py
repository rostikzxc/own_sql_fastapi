from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_name(self, name: str) -> User | None:
        stmt = select(User).where(User.name == name)
        return self.db.scalar(stmt)

    def get_all(self, offset: int = 0, limit: int = 10) -> list[User]:
        stmt = select(User).offset(offset).limit(limit)
        return list(self.db.scalars(stmt))

    def create(self, name: str, hashed_password: str) -> User:
        user = User(name=name, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, name: str | None) -> User:
        if name is not None:
            user.name = name
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_password(self, user: User, hashed_password: str) -> User:
        user.hashed_password = hashed_password
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()