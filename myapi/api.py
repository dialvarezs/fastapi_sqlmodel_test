from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
from myapi.crud import (
    get_group_by_id,
    get_user_by_id,
    insert_group,
    insert_user,
    read_groups,
    read_users,
    update_user,
)

from myapi.database import get_session
from myapi.models import Group, GroupCreate, User, UserBase, UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.get("/users/", response_model=list[UserRead])
async def get_users(session: Session = Depends(get_session)):
    return read_users(session)


@router.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    return insert_user(user, session)


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    try:
        return get_user_by_id(user_id, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch("/users/{user_id}/edit", response_model=User)
async def edit_user(
    user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)
):
    try:
        return update_user(user_id, user_data, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/groups/", response_model=list[Group])
async def get_groups(session: Session = Depends(get_session)):
    return read_groups(session)


@router.get("/groups/{group_id}", response_model=Group)
async def get_group(group_id: int, session: Session = Depends(get_session)):
    try:
        return get_group_by_id(group_id, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Group not found")


@router.post("/groups/", response_model=Group)
async def create_group(group: GroupCreate, session: Session = Depends(get_session)):
    try:
        return insert_group(group, session)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Group already exists")
