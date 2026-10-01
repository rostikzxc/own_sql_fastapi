from pydantic import BaseModel, Field


class RegisterSchema(BaseModel):
    name: str = Field(min_length=4, max_length=22)
    password: str = Field(min_length=5, max_length=22)


class LoginSchema(BaseModel):
    name: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenSchema(BaseModel):
    refresh_token: str