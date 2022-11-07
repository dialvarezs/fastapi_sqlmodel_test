from typing import List

from fastapi import APIRouter, Depends, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session

from myapi.crud import (
    get_group_by_id,
    get_user_by_id,
    insert_group,
    insert_user,
    read_groups,
    read_users,
    update_password,
    update_user,
)
from myapi.database import get_session
from myapi.models import (
    APIToken,
    Group,
    GroupCreate,
    PasswordChange,
    User,
    UserCreate,
    UserRead,
    UserUpdate,
)
from myapi.security import (
    GroupChecker,
    authenticate_user,
    create_jwt,
    get_current_active_user,
)
from myapi.utilities import save_user_image

router = APIRouter()

allow_manage_users = GroupChecker(allowed_groups=["administrators"])


@router.get(
    "/users/",
    response_model=List[UserRead],
)
async def get_users(
    session: Session = Depends(get_session),
):
    return read_users(session)


@router.post(
    "/users/", response_model=UserRead, dependencies=[Depends(allow_manage_users)]
)
async def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
):
    return insert_user(user, session)


@router.get("/users/me", response_model=UserRead)
async def get_user_me(
    user: User = Depends(get_current_active_user),
):
    return user


@router.post("/users/me/change-password/", response_model=UserRead)
async def change_password_me(
    password_change_data: PasswordChange,
    user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    user = update_password(user.id, password_change_data, session)
    return user


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    try:
        return get_user_by_id(user_id, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch(
    "/users/{user_id}/edit",
    response_model=UserRead,
)
async def edit_user(
    user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)
):
    try:
        return update_user(user_id, user_data, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/user/{user_id}/image", response_model=UserRead)
async def set_user_image(
    user_id: int, file: UploadFile, session: Session = Depends(get_session)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")
    image_path = save_user_image(user_id, file)

    return update_user(user_id, UserUpdate(image_path=f"/{image_path}"), session)


@router.get("/groups/", response_model=List[Group])
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


@router.post("/token", response_model=APIToken)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(form_data.username, form_data.password, session)
    token = create_jwt({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
