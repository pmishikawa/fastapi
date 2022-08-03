from pydantic import BaseModel
from datetime import datetime


class JobAlegroLineBase(BaseModel):
    data_job: datetime.date
    title: str
    copies: int
    speed: int
    finished_top_to_bottom: int
    finished_edge: int
    cover_cutting_top: int
    cover_edge: int
    cover_thickness: int
    signature_cutting_top: int
    signature_edge: int
    signature_thickness: int


class JobAlegroLineCreate(JobAlegroLineBase):
    pass


class JobAlegroLine(JobAlegroLineBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
