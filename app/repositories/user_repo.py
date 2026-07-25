from sqlalchemy.orm import Session

from app.models.user import User


# ==========================
# User Repository
# ==========================


# ==========================
# Get Users
# ==========================

def get_by_name(
    db: Session,
    name: str
):
    return (
        db.query(User)
        .filter(User.name == name)
        .first()
    )


def get_all(
    db: Session
):
    return db.query(User).all()


def get_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


# ==========================
# Create User
# ==========================

def create(
    db: Session,
    name: str,
    hashed_password: str
):
    user = User(
        name=name,
        hashed_password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ==========================
# Update User
# ==========================

def update(
    db: Session,
    user_id: int,
    name: str | None
):
    user = get_by_id(
        db,
        user_id
    )

    if not user:
        return None

    if name is not None:
        user.name = name

    db.commit()
    db.refresh(user)

    return user


def update_password(
    db: Session,
    user_id: int,
    hashed_password: str
):
    user = get_by_id(
        db,
        user_id
    )

    if not user:
        return None

    user.hashed_password = hashed_password

    db.commit()
    db.refresh(user)

    return user


# ==========================
# Delete User
# ==========================

def delete(
    db: Session,
    user_id: int
):
    user = get_by_id(
        db,
        user_id
    )

    if not user:
        return None

    db.delete(user)
    db.commit()

    return user