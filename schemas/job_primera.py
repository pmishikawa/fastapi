from pydantic import BaseModel, validator
from datetime import datetime, timedelta, timezone
from typing import Union, Optional

JST = timezone(timedelta(hours=+9), "JST")


class JobPrimeraBase(BaseModel):
    date_job: datetime
    title: Union[str, None] = None
    copies: Union[int, None] = None
    speed: Union[int, None] = None
    finished_top_to_bottom: Union[int, None] = None
    finished_edge: Union[int, None] = None
    has_cut: bool = True
    cutting_top: Union[int, None] = None
    stitches: Union[int, None] = None
    stacks: Union[int, None] = None
    batches: Union[int, None] = None
    cover_cutting_top: Union[int, None] = None
    cover_edge: Union[int, None] = None
    cover_thickness: Union[int, None] = None
    signature_pages: Union[int, None] = None
    signature_top_to_bottom: Union[int, None] = None
    signature_cutting_top: Union[int, None] = None
    signature_cutting_bottom: Union[int, None] = None
    signature_edge: Union[int, None] = None
    signature_thickness: Union[int, None] = None


class JobPrimeraCreate(JobPrimeraBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now(JST)


class JobPrimeraCreateResponse(JobPrimeraCreate):
    id: int

    class Config:
        orm_mode = True


class JobPrimera(JobPrimeraBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
