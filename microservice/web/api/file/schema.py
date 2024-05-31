from datetime import datetime
from pydantic import BaseModel


class PublicFile(BaseModel):
    file_name: str


class File(PublicFile):
    user_id: str
    file_size: float
    file_type: str
    date: datetime