from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from microservice.web.api.file.schema import File
from microservice.db.models import users, files

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_files(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100):
    sql = (
        select(files.File)
        .filter(files.File.user_id == user_id)
        .order_by(files.File.id.desc())
        .slice(skip, skip + limit)
    )
    _files = await db.execute(sql)
    return list(_files.scalar())


async def save_file(db: AsyncSession, file: File):
    db_file = files.File(**file.model_dump())
    db.add(db_file)
    await db.commit()
    return db_file