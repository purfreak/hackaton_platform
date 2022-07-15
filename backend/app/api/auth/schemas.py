from ninja import Schema
from pydantic import EmailStr, validator, BaseModel


class AccessToken(Schema):
    access_token: str


class AuthRequest(BaseModel):
    email: EmailStr
    password: str

    @validator("password", allow_reuse=True)
    def check_password_len(cls, password):
        if len(password) < 6:
            raise ValueError("The password should be at least 6 characters long")

        return password


class RegisterRequest(AuthRequest):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    @validator("password", allow_reuse=True)
    def check_password_len(cls, password):
        if len(password) < 6:
            raise ValueError("The password should be at least 6 characters long")

        return password
