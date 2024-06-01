from datetime import datetime
from pydantic import BaseModel


class PublicFile(BaseModel):
    file_name: str


class File(PublicFile):
    user_id: int
    file_size: float
    file_type: str
    file_path: str
    date: datetime