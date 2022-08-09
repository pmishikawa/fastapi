import email
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from fastapi import HTTPException, status
from typing import Tuple, Optional
from passlib.context import CryptContext
from lib.auth_utils import AuthJwtCsrf
import cruds.user as user_crud
import models.user as user_model

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth = AuthJwtCsrf()

# async def signup(db: AsyncSession, data: dict) -> dict:
#     email = data.get("email")
#     password = data.get("password")
#     overlap_user = await user_crud.get_user_by_email(db, email)
#     if overlap_user:
#         raise HTTPException(status_code=400, detail="Email is already taken")
#     if not password or len(password) < 6:
#         raise HTTPException(status_code=400, detail="Password too short")


async def login(db: AsyncSession, user: user_model.User) -> str:

    email = user.email
    password = user.password

    print("------------------->1")
    print(email)
    print(password)
    login_user = await user_crud.get_user_by_email(db, email)

    print("------------------->2")
    print(login_user)
    if not login_user or not auth.verify_password(password, login_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    print(login_user.email)
    print("------------------->3")
    token = auth.encode_jwt(login_user.email)
    print("------------------->4")
    print(token)
    return token


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(
    db: AsyncSession, email: str, password: str, expire: int, reuse: bool
):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True


def generate_hashed_password(password):
    return pwd_context.hash(password)