from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from microservice.db.dependencies import get_db_session
from microservice.web.api.user.schema import UserCreate, User

router = APIRouter()


@router.post("/create", include_in_schema=False)
async def create_user(user: UserCreate, db: Session = Depends(get_db_session)) -> User:
    """
    Создание пользователя
    """
    

