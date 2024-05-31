from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from microservice.web.api.file.schema import File
from microservice.db.models import users, files

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_files(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    sql = (
        select(files.File)
        .filter(files.File.user_id == user_id)
        .order_by(files.File.id.desc())
        .slice(skip, skip + limit)
    )
    _files = await db.execute(sql)
    scalar = list(_files.scalar())
    if scalar[0]:
        return scalar
    else:
        return []

async def get_file(db: AsyncSession, user_id: int, file_name: str):
    sql = (
        select(files.File)
        .filter(files.File.user_id == user_id)
        .filter(files.File.file_name == file_name)
    )
    file = await db.execute(sql)
    return file.scalar()

async def save_file(db: AsyncSession, file: File):
    db_file = files.File(**file.model_dump())
    db.add(db_file)
    await db.commit()
    return db_file


async def del_file(db: AsyncSession, user_id: int, file_id: int):
    sql = (
        select(files.File)
        .filter(files.File.user_id == user_id)
        .filter(files.File.id == file_id)
    )
    file = await db.execute(sql)
    db.delete(file)