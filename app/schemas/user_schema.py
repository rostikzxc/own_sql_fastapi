from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    name: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    role: str

    model_config = ConfigDict(
        from_attributes=True
    )

class UserUpdate(BaseModel):
    name: str | None = None

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str