from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from myapi.models import Group, GroupCreate, User, UserBase, UserCreate, UserUpdate


def read_users(session: Session):
    query = select(User)
    return session.execute(query).scalars().all()


def insert_user(user: UserCreate, session: Session):
    user_db = User(**user.dict(exclude_unset=True, exclude={"group_ids"}))
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


def update_user(user_id: int, user_data: UserUpdate, session: Session) -> User:
    user_db = get_user_by_id(user_id, session)
    for field, value in user_data.dict(exclude_none=True).items():
        setattr(user_db, field, value)
    session.commit()

    return user_db


def read_groups(session: Session):
    query = select(Group)
    return session.execute(query).scalars().all()


def get_group_by_id(group_id: int, session: Session) -> Group:
    query = select(Group).where(Group.id == group_id)
    return session.execute(query).scalar_one()


def insert_group(group: GroupCreate, session: Session):
    group_db = Group(**group.dict(exclude_unset=True))
    session.add(group_db)
    session.commit()

    return group_db