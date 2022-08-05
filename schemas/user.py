from pydantic import BaseModel, Field
from schemas.item import Item
from typing import Union, Optional


class UserBase(BaseModel):
    email: Optional[str] = "test@example.com"


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: Union[int, None] = None
    is_active: Union[bool, None] = Field(None, example="True", description="フラグ")
    items: list[Item] = []

    class Config:
        orm_mode = True
