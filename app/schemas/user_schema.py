from pydantic import BaseModel, ConfigDict, Field

from app.models.user import UserRole


class UserCreate(BaseModel):
    name: str = Field(min_length=4, max_length=12)
    password: str = Field(min_length=5, max_length=22)


class UserResponse(BaseModel):
    id: int
    name: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=4, max_length=12)


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str = Field(min_length=5, max_length=22)