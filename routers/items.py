from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import get_db
import api.schemas.item as item_schema
import api.cruds.item as item_crud

router = APIRouter()


@router.get("/items/", response_model=list[item_schema.Item])
async def read_items(skip: int = 0, limit: int = 0, db: AsyncSession = Depends(get_db)):
    items = await item_crud.get_items(db, skip=skip, limit=limit)

    print(items)
    return items
