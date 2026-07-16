from app.models.user import User
from sqlalchemy.orm import Session

def get_all(db: Session):
    return db.query(User).all()

def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def delete(db: Session, user_id: int):
    find_user_by_id = db.query(User).filter(User.id == user_id).first()

    if not find_user_by_id:
        return None

    db.delete(find_user_by_id)
    db.commit()

def update(db: Session, name, hashed_password, user_id: int):
    find_user_by_id = db.query(User).filter(User.id == user_id).first()

    if not find_user_by_id:
        return None

    find_user_by_id.name = name
    find_user_by_id.hashed_password = hashed_password

    db.commit()
    
    return(find_user_by_id)

def create(db: Session, name: str, hashed_password: str):
    user = User(
        name=name,
        hashed_password=hashed_password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user