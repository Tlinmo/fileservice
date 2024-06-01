from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from microservice.web.api.user.schema import UserCreate, UserUpdate
from microservice.db.models import users
from microservice.db.dependencies import get_db_session
from microservice.settings import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from microservice.settings import settings
from microservice.web.api.user.schema import TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


async def authenticate_user(db, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.users_secret, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = users.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    return db_user


async def get_user_by_id(db: AsyncSession, user_id: int):
    return await db.get(users.User, user_id)


async def get_user_by_username(db: AsyncSession, username: str):
    sql = select(users.User).filter(users.User.username == username)
    questions = await db.execute(sql)
    return questions.scalars().one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    sql = select(users.User).order_by(users.User.id.desc()).slice(skip, skip + limit)
    _users = await db.execute(sql)
    return list(_users.scalars())


async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    db_user = await get_user_by_id(db, user_id)
    if db_user:
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        await db.commit()
    return db_user