from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


# ==========================
# User Model
# ==========================

class User(Base):
    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String,
        nullable=False
    )


    hashed_password = Column(
        String,
        nullable=False
    )


    role = Column(
        String,
        default="user",
        nullable=False
    )


    refresh_token = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )