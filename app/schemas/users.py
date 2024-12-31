from pydantic import BaseModel, EmailStr


class EmailToken(BaseModel):
    email: EmailStr
    identity_token: str


class UserBase(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    intro: str | None = None
    identity_token: str | None = None
