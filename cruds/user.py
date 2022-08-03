from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
import schemas.user as user_schema
import models.user as user_model
import models.item as item_model


async def get_user(db: AsyncSession, user_id: int):
    result: Result = await db.execute(
        select(
            user_model.User.id,
            user_model.User.email,
            user_model.User.is_active,
            item_model.Item,
        ).outerjoin(
            item_model.Item,
            user_model.User.id == item_model.Item.owner_id,
        )
    )
    # for item in result:
    #    print(item.Item.id)

    return result.first()


async def get_user_by_email(db: AsyncSession, email: str):
    return (
        await db.query(user_model.User).filter(user_model.User.email == email).filter()
    )


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):

    result: Result = await db.execute(
        select(user_model.User).offset(skip).limit(limit).all()
    )

    return await result


async def create_user(db: AsyncSession, user: user_schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = await user_model.User(
        email=user.email, fake_hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
