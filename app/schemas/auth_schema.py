from pydantic import BaseModel

class RegisterSchema(BaseModel):
    name: str
    password: str

class LoginSchema(BaseModel):
    name: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class RefreshTokenSchema(BaseModel):
    refresh_token: str