from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(max_length=32, unique=True, index=True)
    fullname: str = Field(max_length=64)
    age: Optional[int]


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, default=None)
    is_active: bool = Field(default=True)


class UserUpdate(SQLModel):
    username: Optional[str] = Field(max_length=32)
    fullname: Optional[str] = Field(max_length=64)
    age: Optional[int]
    is_active: Optional[bool]
