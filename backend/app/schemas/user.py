from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole
from app.schemas.common import TimestampedRead


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    phone: str | None = None
    role: UserRole = UserRole.FARMER


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserRead(UserBase, TimestampedRead):
    is_active: bool
