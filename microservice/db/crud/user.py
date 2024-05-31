from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from microservice.web.api.user.schema import UserCreate
from microservice.db.models import users
from microservice.web.api.user.schema import PublicUser


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(db, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, str(user.hashed_password)):
        return False
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
    sql = (
        select(users.User)
        .filter(users.User.username == username)
    )
    questions = await db.execute(sql)
    return questions.scalars().one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    sql = select(users.User).order_by(users.User.id.desc()).slice(skip, skip + limit)
    _users = await db.execute(sql)
    return list(_users.scalars())


