from datetime import datetime, timedelta, timezone
from typing import Annotated, List
import io

from fastapi import APIRouter, Depends, HTTPException, status, File as FFile, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from microservice.web.api.file.schema import PublicFile, File
from microservice.web.api.user.schema import UserCreate, PrivateUser, Token, TokenData, PublicUser
from microservice.db.dependencies import get_db_session
from microservice.db import crud
from microservice.settings import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from microservice.settings import settings
from utils.file import save, _path_to_file, read_compress_file, read_encrypt_compress_file, delete


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
    
    
@router.post("/upload_file")
async def upload_files(
    current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)],
    file: UploadFile = FFile(...),
    db: AsyncSession = Depends(get_db_session)
):
    file_type = file.filename.split(".")[-1]
    if file_type in current_user.file_type or current_user.file_type == ["*"]:
        if not (await crud.file.get_file(db, current_user.id, file.filename)):
            file_size = save(
                file,
                file.filename,
                current_user.id,
                True,
                current_user.crypt_file
            )
            await crud.file.save_file(
                db,
                File(
                    file_name=file.filename,
                    user_id=current_user.id,
                    file_size=file_size,
                    file_type=file_type,
                    date=datetime.now()
                )
            )
        else:
            raise HTTPException(400, "File already exited")
    else:
        raise HTTPException(403, "File type not accepted")


@router.post("/get_file")
async def get_file(
    current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)],
    file: PublicFile,
    db: AsyncSession = Depends(get_db_session)
):
    file = await crud.file.get_file(db, current_user.id, file.file_name)
    if file:
        path = _path_to_file(file.file_type, file.file_name, current_user.id)
        
        if current_user.crypt_file:
            file_b = read_encrypt_compress_file(path)
        else:
            file_b = read_compress_file(path)
        file_b = io.BytesIO(file_b)
        
        return StreamingResponse(
            file_b,
            media_type='application/octet-stream',
            headers={"Content-Disposition": f"attachment; filename={file.file_name}"}
            )
    else:
        raise HTTPException(400, "File not Found")
            


@router.post("/del_file")
async def del_file(
    current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)],
    file_p: PublicFile,
    db: AsyncSession = Depends(get_db_session)
):
    file = await crud.file.get_file(db, current_user.id, file_p.file_name)
    if file:
        delete(_path_to_file(file.file_type, file.file_name, current_user.id))
        await crud.file.del_file(db, current_user.id, file.id)
    else:
        raise HTTPException(400, "File not Found")