import pytest
from fastapi.testclient import TestClient
import uuid
from app.models.user import User
from app.core.security import hash_password
from app.core.database import SessionLocal

from app.main import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def test_user():
    return {
        "name": f"arthas_{uuid.uuid4()}",
        "password": "1911"
    }

@pytest.fixture
def db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def admin_user(db):

    name = f"admin_{uuid.uuid4()}"

    user = User(
        name=name,
        hashed_password=hash_password("1911"),
        role="admin"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": name,
        "password": "1911"
    }