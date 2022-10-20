from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class UserGroupLink(SQLModel, table=True):
    __tablename__ = "users_groups"

    user_id: int = Field(primary_key=True, foreign_key="users.id")
    group_id: int = Field(primary_key=True, foreign_key="groups.id")


class UserBase(SQLModel):
    username: str = Field(max_length=32, unique=True, index=True)
    fullname: str = Field(max_length=64)
    age: Optional[int]


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, default=None)
    password: str = Field(max_length=256, nullable=True)
    is_active: bool = Field(default=True)

    groups: List["Group"] = Relationship(
        back_populates="users", link_model=UserGroupLink
    )


class UserRead(UserBase):
    id: int
    is_active: bool
    groups: List["Group"]


class UserCreate(UserBase):
    password: str = Field(max_length=256, nullable=True)
    group_ids: List[int] = []


class UserUpdate(SQLModel):
    username: Optional[str] = Field(max_length=32)
    fullname: Optional[str] = Field(max_length=64)
    age: Optional[int]
    is_active: Optional[bool]
    groups_ids: Optional[List[int]]


class GroupBase(SQLModel):
    name: str = Field(max_length=32, unique=True, index=True)


class Group(GroupBase, table=True):
    __tablename__ = "groups"

    id: int = Field(primary_key=True, default=None)
    is_active: bool = Field(default=True)

    users: List["User"] = Relationship(
        back_populates="groups", link_model=UserGroupLink
    )


class GroupCreate(GroupBase):
    pass


class GroupUpdate(SQLModel):
    name: Optional[str] = Field(max_length=32)
    is_active: Optional[bool]


class APIToken(SQLModel):
    access_token: str
    token_type: str


UserRead.update_forward_refs()
