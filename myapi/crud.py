from sqlalchemy import select
from sqlmodel import Session

from myapi.models import User, UserBase


def read_users(session: Session):
    query = select(User)
    return session.execute(query).scalars().all()


def insert_user(user: UserBase, session: Session):
    user_db = User(**user.dict(exclude_unset=True))
    session.add(user_db)
    session.commit()

    return user_db

def get_user_by_id(user_id: int, session: Session):
    query = select(User).where(User.id == user_id)
    return session.execute(query).scalar_one()