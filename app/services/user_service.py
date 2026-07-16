from app.repositories.user_repo import get_all, create
from app.core.security import hash_password
from sqlalchemy.orm import Session

def get_users(db: Session):
    return get_all(db)

def create_user(db: Session, name: str, password: str):
    hashed_password = hash_password(password)
    return create(db, name, hashed_password)
