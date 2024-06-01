from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from microservice.web.api.user.schema import UserUpdate, PrivateUser
from microservice.db.dependencies import get_db_session
from microservice.db import crud


router = APIRouter()


@router.post("/user/{user_id:int}/update")
async def read_user(
    user_id: int,
    user: UserUpdate,
    current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)],
    db: AsyncSession = Depends(get_db_session),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Permision denied")
    
    db_user = await crud.user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_user =  await crud.user.update_user(db, user_id=user_id, user_update=user)
    return update_user


# @router.get("/{user_id:int}")
# async def read_user(
#     user_id: int,
#     current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)],
#     db: AsyncSession = Depends(get_db_session),
# ):
#     db_user = await crud.user.get_user_by_id(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
