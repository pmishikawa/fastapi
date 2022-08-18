from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import Tuple, Optional
import schemas.user as user_schema
import models.user as user_model
from lib.auth_utils import AuthJwtCsrf

# from fastapi.encoders import jsonable_encoder
auth = AuthJwtCsrf()

"""
def user_serializer(users) -> dict:
    result = []
    items = []
    tmp_id = None
    for user in users:
        tmp_id = user.Item.id
        print("-----------------------1")
        print(user.Item.id)

        if tmp_id == user.Item.id:
            item_values = {
                "id": str(user.Item.id),
                "title": user.Item.title,
                "description": bool(user.Item.description),
                "owner_id": user.Item.owner_id,
            }

            items.append(item_values)
            print("-----------------------2")
            print(items)
        else:

            values = {
                "id": str(user.User.id),
                "email": user.User.email,
                "is_active": bool(user.User.is_active),
                "items": items,
            }
            result.append(values)

            items = []
            item_values = {
                "id": str(user.Item.id),
                "title": user.Item.title,
                "description": bool(user.Item.description),
                "owner_id": user.Item.owner_id,
            }
            items.append(item_values)

            print("-----------------------3")
            print(result)

    print("-----------------------4")
    print(items)
    if items:
        values = {
            "id": str(user.User.id),
            "email": user.User.email,
            "is_active": bool(user.User.is_active),
            "items": items,
        }
        result.append(values)

        print("-----------------------5")
        print(result)

        print("===")
        print(result)

    return result
"""

"""
async def get_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Optional[user_model.User]:

    # result: Result = await db.execute(select(user_model.User).offset(skip).limit(limit))
    result: Ressault = await db.execute(
        select(user_model.User, item_model.Item)
        .select_from(user_model.User)
        .join(
            item_model.Item,
            user_model.User.id == item_model.Item.owner_id,
        )
        .order_by(user_model.User.id)
    )
    # print(result.all())
    # print("---------------------------test")
    # return result.all()

    users: Optional[List[user_model.User]] = result.all()

    return user_serializer(users)

    # return user[0] if user is not None else None
"""


async def get_user(db: AsyncSession, user_id: int):
    result: Result = await db.execute(
        select(user_model.User)
        .select_from(user_model.User)
        .where(user_model.User.id == user_id)
    )

    user = result.first()
    return user[0].toDict() if user is not None else None


async def get_user_by_email(db: AsyncSession, email: str):

    result: Result = await db.execute(
        select(user_model.User)
        .select_from(user_model.User)
        .where(user_model.User.email == email)
    )

    user = result.first()
    return user[0].toDict() if user is not None else None


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):

    result: Result = await db.execute(
        select(
            user_model.User.id,
            user_model.User.email,
            user_model.User.is_active,
            user_model.User.created_at,
            user_model.User.updated_at,
        )
        .offset(skip)
        .limit(limit)
    )
    return result.all()


async def create_user(
    db: AsyncSession, user: user_schema.UserCreate
) -> user_model.User:

    user = user_model.User(
        email=user.email,
        hashed_password=auth.generate_hashed_password(user.hashed_password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


"""
async def create_user_item(
    db: AsyncSession, item: item_schema.ItemCreate, user_id: int
):

    print("---------------------------1")
    print(user_id)
    print("---------------------------2")
    print(type(item))
    print("---------------------------3")
    test = item.dict()
    print(type(test))
    db_item = item_model.Item(id=1, title="aaaa", description="www", owner_id=user_id)
    # db_item = item_model.Item(item.dict(), owner_id=user_id)
    print("---------------------------4")
    print(db_item)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
"""
