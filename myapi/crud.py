from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from myapi.models import (
    Group,
    GroupCreate,
    Note,
    NoteCreate,
    NoteUpdate,
    PasswordChange,
    User,
    UserCreate,
    UserUpdate,
)
from myapi.security import auth_exception, hash_password, verify_password


def select_users(session: Session) -> List[User]:
    query = select(User)
    return session.execute(query).scalars().all()


def insert_user(user: UserCreate, session: Session) -> User:
    user_db = User(**user.dict(exclude_unset=True, exclude={"group_ids"}))
    user_db.password = hash_password(user.password)
    for group_id in user.group_ids:
        try:
            group = select_group_by_id(group_id, session)
            user_db.groups.append(group)
        except NoResultFound:
            pass
    session.add(user_db)
    session.commit()

    return user_db


def select_user_by_id(user_id: int, session: Session) -> User:
    query = select(User).where(User.id == user_id)
    return session.execute(query).scalar_one()


def select_user_by_username(username: str, session: Session) -> User:
    query = select(User).where(User.username == username)
    return session.execute(query).scalar_one()


def update_user(user_id: int, user_data: UserUpdate, session: Session) -> User:
    user_db = select_user_by_id(user_id, session)
    for field, value in user_data.dict(exclude_none=True).items():
        if field == "group_ids":
            user_db.groups = []
            for group_id in value:
                try:
                    group = select_group_by_id(group_id, session)
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
    user_db = select_user_by_id(user_id, session)
    if not verify_password(change_password_data.old_password, user_db.password):
        raise auth_exception("Invalid password")
    user_db.password = hash_password(change_password_data.new_password)
    session.commit()

    return user_db


def select_groups(session: Session) -> List[Group]:
    query = select(Group)
    return session.execute(query).scalars().all()


def select_group_by_id(group_id: int, session: Session) -> Group:
    query = select(Group).where(Group.id == group_id)
    return session.execute(query).scalar_one()


def insert_group(group: GroupCreate, session: Session) -> Group:
    group_db = Group(**group.dict(exclude_unset=True))
    session.add(group_db)
    session.commit()

    return group_db


def insert_note(note_data: NoteCreate, user: User, session: Session) -> Note:
    note = Note(**note_data.dict(exclude_unset=True))
    note.user = user
    session.add(note)
    session.commit()

    return note


def update_note(note_id: int, note_data: NoteUpdate, session: Session) -> Note:
    note = select_note_by_id(note_id, session)
    for field, value in note_data.dict(exclude_none=True).items():
        setattr(note, field, value)
    session.commit()

    return note


def select_note_by_id(note_id: int, session: Session) -> Note:
    query = select(Note).where(Note.id == note_id)
    return session.execute(query).scalar_one()


def select_user_notes(
    user_id: int, session: Session, archived: Optional[bool]
) -> List[Note]:
    query = select(Note).where(Note.user_id == user_id)
    if archived is not None:
        query = query.where(Note.is_archived == archived)
    return session.execute(query).scalars().all()


def select_notes(session: Session) -> List[Note]:
    query = select(Note)
    return session.execute(query).scalars().all()


def select_public_notes(session: Session) -> List[Note]:
    query = select(Note).where(Note.is_public == True)
    return session.execute(query).scalars().all()
