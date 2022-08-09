from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: Optional[str] = "test@example.com"


class UserCreate(UserBase):
    hashed_password: str


class UserCreateResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
