from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class PublicUser(UserBase):
    id: int
    is_superuser: bool


class PrivateUser(UserBase):
    id: int
    hashed_password: str
    is_superuser: bool = False
    file_type: list[str] = ["*"]
    file_size: int = -1
    can_delete: bool = False
    jpg_quality: int = 100
    crypt_file: bool = False


class UserUpdate(BaseModel):
    file_type: list[str] = ["*"]
    file_size: int = -1
    can_delete: bool = False
    crypt_file: bool = False
