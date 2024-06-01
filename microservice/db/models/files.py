from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, ARRAY, Double, DateTime
from sqlalchemy.orm import relationship

from microservice.db.base import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    file_size = Column(Double, index=True)
    file_type = Column(String, index=True)
    file_path = Column(String, index=True)
    file_name = Column(String, index=True)
    date = Column(DateTime, index=True)
    