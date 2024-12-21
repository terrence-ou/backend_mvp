from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr | None = None
    username: str | None = None


class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
