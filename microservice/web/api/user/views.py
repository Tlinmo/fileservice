from datetime import datetime, timedelta, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from microservice.web.api.user.schema import UserCreate, PrivateUser, Token, PublicUser
from microservice.db.dependencies import get_db_session
from microservice.db import crud
from microservice.settings import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from microservice.settings import settings


router = APIRouter()


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.users_secret, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db_session),
) -> Token:
    user = await crud.user.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
        },
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=PrivateUser)
async def read_users_me(current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)]):
    return current_user


@router.post("/create", response_model=PrivateUser)
async def api_create_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    db_user = await crud.user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud.user.create_user(db=db, user=user)


# API для вывода всех пользователей, быть может следует сделать проверку на Админа?
@router.get("/users/", response_model=List[PublicUser])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)):
    users = await crud.user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id:int}", response_model=PublicUser)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    db_user = await crud.user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
