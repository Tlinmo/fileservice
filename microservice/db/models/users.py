from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, ARRAY
from sqlalchemy.orm import relationship

from microservice.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, index=True)
    is_superuser = Column(Boolean, default=False)
    file_type = Column(ARRAY(String), default=[".*"])
    file_size = Column(Integer, default=-1)
    can_delete = Column(Boolean, default=False)
    jpg_quality = Column(Integer, default=100)
    hash_file = Column(Boolean, default=False)
    



# # type: ignore
# import uuid

# from fastapi import Depends
# from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, schemas
# from fastapi_users.authentication import (
#     AuthenticationBackend,
#     BearerTransport,
#     JWTStrategy,
# )
# from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
# from sqlalchemy.ext.asyncio import AsyncSession

# from microservice.db.base import Base
# from microservice.db.dependencies import get_db_session
# from microservice.settings import settings


# class User(SQLAlchemyBaseUserTableUUID, Base):
#     """Represents a user entity."""


# class UserRead(schemas.BaseUser[uuid.UUID]):
#     """Represents a read command for a user."""


# class UserCreate(schemas.BaseUserCreate):
#     """Represents a create command for a user."""


# class UserUpdate(schemas.BaseUserUpdate):
#     """Represents an update command for a user."""


# class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
#     """Manages a user session and its tokens."""

#     reset_password_token_secret = settings.users_secret
#     verification_token_secret = settings.users_secret


# async def get_user_db(
#     session: AsyncSession = Depends(get_db_session),
# ) -> SQLAlchemyUserDatabase:
#     """
#     Yield a SQLAlchemyUserDatabase instance.

#     :param session: asynchronous SQLAlchemy session.
#     :yields: instance of SQLAlchemyUserDatabase.
#     """
#     yield SQLAlchemyUserDatabase(session, User)


# async def get_user_manager(
#     user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
# ) -> UserManager:
#     """
#     Yield a UserManager instance.

#     :param user_db: SQLAlchemy user db instance
#     :yields: an instance of UserManager.
#     """
#     yield UserManager(user_db)


# def get_jwt_strategy() -> JWTStrategy:
#     """
#     Return a JWTStrategy in order to instantiate it dynamically.

#     :returns: instance of JWTStrategy with provided settings.
#     """
#     return JWTStrategy(secret=settings.users_secret, lifetime_seconds=None)


# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
# auth_jwt = AuthenticationBackend(
#     name="jwt",
#     transport=bearer_transport,
#     get_strategy=get_jwt_strategy,
# )

# backends = [
#     auth_jwt,
# ]

# api_users = FastAPIUsers[User, uuid.UUID](get_user_manager, backends)

# current_active_user = api_users.current_user(active=True)
