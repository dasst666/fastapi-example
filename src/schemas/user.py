from typing import Optional
from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field

from enum import Enum

class UserBase(SQLModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль должен быть более 8 символов")
        if not any(c.isdigit() for c in v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(c.isupper() for c in v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        return v

class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    role: RoleEnum = Field(default=RoleEnum.user)

class UserPublic(UserBase):
    id: int
    