from pydantic import BaseModel
from datetime import datetime
from typing import Union


class JobPrimeraBase(BaseModel):
    data_job: datetime
    title: Union[str, None] = None
    copies: Union[int, None] = None
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
    pass


class JobPrimera(JobPrimeraBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
