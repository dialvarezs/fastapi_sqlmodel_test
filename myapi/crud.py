from typing import List
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from myapi.models import (
    Group,
    GroupCreate,
    PasswordChange,
    User,
    UserCreate,
    UserUpdate,
)
from myapi.security import auth_exception, hash_password, verify_password


def read_users(session: Session) -> List[User]:
    query = select(User)
    return session.execute(query).scalars().all()


def insert_user(user: UserCreate, session: Session) -> User:
    user_db = User(**user.dict(exclude_unset=True, exclude={"group_ids"}))
    user_db.password = hash_password(user.password)
    for group_id in user.group_ids:
        try:
            group = get_group_by_id(group_id, session)
            user_db.groups.append(group)
        except NoResultFound:
            pass
    session.add(user_db)
    session.commit()

    return user_db


def get_user_by_id(user_id: int, session: Session) -> User:
    query = select(User).where(User.id == user_id)
    return session.execute(query).scalar_one()


def get_user_by_username(username: str, session: Session) -> User:
    query = select(User).where(User.username == username)
    return session.execute(query).scalar_one()


def update_user(user_id: int, user_data: UserUpdate, session: Session) -> User:
    user_db = get_user_by_id(user_id, session)
    for field, value in user_data.dict(exclude_none=True).items():
        if field == "group_ids":
            user_db.groups = []
            for group_id in value:
                try:
                    group = get_group_by_id(group_id, session)
                    user_db.groups.append(group)
                except NoResultFound:
                    pass
        else:
            setattr(user_db, field, value)
    session.commit()

    return user_db


def update_password(
    user_id: int, change_password_data: PasswordChange, session: Session
) -> User:
    user_db = get_user_by_id(user_id, session)
    if not verify_password(change_password_data.old_password, user_db.password):
        raise auth_exception("Invalid password")
    user_db.password = hash_password(change_password_data.new_password)
    session.commit() 

    return user_db


def read_groups(session: Session) -> List[Group]:
    query = select(Group)
    return session.execute(query).scalars().all()


def get_group_by_id(group_id: int, session: Session) -> Group:
    query = select(Group).where(Group.id == group_id)
    return session.execute(query).scalar_one()


def insert_group(group: GroupCreate, session: Session) -> Group:
    group_db = Group(**group.dict(exclude_unset=True))
    session.add(group_db)
    session.commit()

    return group_db
