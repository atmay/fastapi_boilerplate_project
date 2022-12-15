from datetime import datetime as dt
from pydantic import BaseModel


class _PostBase(BaseModel):
    title: str
    content: str


class PostCreate(_PostBase):
    pass


class Post(_PostBase):
    id: int
    owner_id: int
    date_created: dt
    date_last_updated: dt

    class Config:
        orm_mode = True


class _UserBase(BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_active: bool
    posts: list[Post] = []

    class Config:
        orm_mode = True
