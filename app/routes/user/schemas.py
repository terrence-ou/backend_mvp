from pydantic import BaseModel, EmailStr


class EmailToken(BaseModel):
    email: EmailStr
    session_token: str


class UserBase(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    intro: str | None = None
    session_token: str | None = None


class SessionToken(BaseModel):
    session_token: str


class ValidationResponse(BaseModel):
    valid: bool
    message: str
