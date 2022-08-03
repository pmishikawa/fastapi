from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import schemas.user as user_schema
import schemas.item as item_schema
import cruds.user as user_crud

router = APIRouter()


@router.post("/users/", response_model=user_schema.User)
async def create_user(user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)


@router.get("/users", response_model=list[user_schema.User])
async def read_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    users = await user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=user_schema.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items/", response_model=user_schema.Item)
async def create_item_for_user(
    user_id: int, item: item_schema.ItemCreate, db: AsyncSession = Depends(get_db)
):
    return await user_crud.create_user_item(db=db, item=item, user_id=user_id)
