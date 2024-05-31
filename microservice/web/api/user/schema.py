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
    is_superuser: bool
    hashed_password: str
