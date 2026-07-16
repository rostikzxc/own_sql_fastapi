from fastapi import APIRouter, Depends
from app.services import user_service
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["USER"])

@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.post("")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user.name, user.password)
