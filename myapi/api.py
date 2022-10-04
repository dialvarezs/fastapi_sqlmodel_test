from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session
from sqlalchemy.exc import NoResultFound
from myapi.crud import get_user_by_id, insert_user, read_users

from myapi.database import get_session
from myapi.models import User, UserBase

router = APIRouter()


@router.get("/users/", response_model=list[User])
async def get_users(session: Session = Depends(get_session)):
    return read_users(session)


@router.post("/users/", response_model=User)
async def create_user(user: UserBase, session: Session = Depends(get_session)):
    return insert_user(user, session)


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    try:
        return get_user_by_id(user_id, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
