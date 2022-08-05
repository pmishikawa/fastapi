from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from fastapi.encoders import jsonable_encoder
from typing import List, Tuple, Optional
import schemas.user as user_schema
import schemas.item as item_schema
import models.user as user_model
import models.item as item_model


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


async def get_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Optional[user_model.User]:

    # result: Result = await db.execute(select(user_model.User).offset(skip).limit(limit))
    result: Result = await db.execute(
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


async def get_user(db: AsyncSession, user_id: int):
    result: Result = await db.execute(
        select(
            user_model.User.id,
            user_model.User.email,
            user_model.User.is_active,
            item_model.Item.id,
        )
        .select_from(user_model.User)
        .outerjoin(
            item_model.Item,
            user_model.User.id == item_model.Item.owner_id,
        )
        .where(user_model.User.id == user_id)
    )

    # for item in result:
    #    print(item.Item.id)
    # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す

    user: Optional[Tuple[user_model.Task]] = result.first()
    print(user)
    print("---------------------------112")
    return user[0] if user is not None else None


async def get_user_by_email(db: AsyncSession, email: str):

    result: Result = await db.execute(
        select(
            user_model.User.id,
        )
        .select_from(user_model.User)
        .where(user_model.User.email == email)
    )

    row = result.first()
    print("---------------------------11")
    print(row)
    print("---------------------------22")
    # del result
    return row
    # return (
    #    await db.query(user_model.User).filter(user_model.User.email == email).filter()
    # )


async def create_user(db: AsyncSession, user: user_schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    # user_data = jsonable_encoder(user)

    db_user = user_model.User(email=user.email, hashed_password=fake_hashed_password)
    print("---------------------------test")
    # print(type(user_data))
    print(db_user.email)
    print("---------------------------test")

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


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
