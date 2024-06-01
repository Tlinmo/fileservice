from datetime import datetime
from pydantic import BaseModel


class PublicFile(BaseModel):
    file_name: str


class File(PublicFile):
    user_id: int
    file_size: float
    file_path: str
    file_type: str
    date: datetime