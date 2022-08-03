from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.engine import Result

# import api.schemas.item as item_schema
import api.models.item as item_model


async def get_items(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[Tuple[int, str, str, int]]:
    result: Result = await db.execute(
        select(
            item_model.Item.id,
            item_model.Item.title,
            item_model.Item.description,
            item_model.Item.owner_id,
        )
    )

    return result.all()
