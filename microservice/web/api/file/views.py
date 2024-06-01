from datetime import datetime
from typing import Annotated, List
import io

from fastapi import APIRouter, Depends, HTTPException, File as FFile, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from microservice.web.api.file.schema import PublicFile, File
from microservice.web.api.user.schema import PrivateUser
from microservice.db.dependencies import get_db_session
from microservice.db import crud
from utils.file import reader, save, _path_to_file, delete


router = APIRouter()


@router.get("/get_files", response_model=List[File])
async def get_files(
    current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)],
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session),
):
    if current_user.id == user_id or current_user.is_superuser:
        return await crud.file.get_files(db, user_id, skip, limit)
    else:
        raise HTTPException(403, "You have no permission!")


@router.post("/upload_file")
async def upload_files(
    current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)],
    file: UploadFile = FFile(...),
    db: AsyncSession = Depends(get_db_session),
):
    file_type = file.filename.split(".")[-1]
    if file_type in current_user.file_type or current_user.file_type == ["*"]:
        if not (await crud.file.get_file(db, current_user.id, file.filename)):
            file_data = save(
                file=file,
                user_id=current_user.id,
                size_limit=current_user.file_size,
                zipped=True,
                encrypted=current_user.crypt_file,
            )
            if file_data["file_size"] == -1:
                raise HTTPException(403, "File size out of limit")

            await crud.file.save_file(
                db,
                File(
                    file_name=file.filename,
                    file_path=file_data["path"],
                    user_id=current_user.id,
                    file_size=file_data["file_size"],
                    file_type=file_type,
                    date=datetime.now(),
                ),
            )
        else:
            raise HTTPException(400, "File already exited")
    else:
        raise HTTPException(403, "File type not accepted")


@router.post("/get_file")
async def get_file(
    current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)],
    _file: PublicFile,
    db: AsyncSession = Depends(get_db_session),
):
    file = await crud.file.get_file(db, current_user.id, _file.file_name)
    if file:
        file_b = reader(file.file_path)
        file_b = io.BytesIO(file_b)

        return StreamingResponse(
            file_b,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file.file_name}"},
        )
    else:
        raise HTTPException(400, "File not Found")


@router.post("/del_file")
async def del_file(
    current_user: Annotated[PrivateUser, Depends(crud.user.get_current_user)],
    file_p: PublicFile,
    db: AsyncSession = Depends(get_db_session),
):
    if current_user.can_delete:
        file = await crud.file.get_file(db, current_user.id, file_p.file_name)
        if file:
            delete(
                _path_to_file(
                    file.file_type,
                    (
                        file.file_name + ".gz" + ".encrypted"
                        if current_user.crypt_file
                        else ""
                    ),
                    current_user.id,
                )
            )
            await crud.file.del_file(db, current_user.id, file.id)
        else:
            raise HTTPException(400, "File not Found")
    else:
        raise HTTPException(403, "You cannot delete file")
