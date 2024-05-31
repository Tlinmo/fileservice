from datetime import datetime, timedelta, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from microservice.web.api.file.schema import PublicFile, File
from microservice.web.api.user.schema import UserCreate, PrivateUser, Token, TokenData, PublicUser
from microservice.db.dependencies import get_db_session
from microservice.db import crud
from microservice.settings import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from microservice.settings import settings


router = APIRouter()


@router.get("/get_files", response_model=List[File])
async def get_files(
    current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)],
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session)
    ):
    if current_user.id == user_id or current_user.is_superuser:
        return await crud.file.get_files(db, current_user.id, skip, limit)
    else:
        raise HTTPException(403, "You have no permission!")