from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    intro: str | None = None
