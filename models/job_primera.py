from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.types import TIMESTAMP
from database import Base
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")


class JobPrimera(Base):
    __tablename__ = "job_primera"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    data_job = Column(type_=TIMESTAMP(timezone=True))
    title = Column(String(255), default="")
    copies = Column(Integer, default=0)
    speed = Column(Integer, default=0)
    finished_top_to_bottom = Column(Integer, default=0)
    finished_edge = Column(Integer, default=0)
    has_cut = Column(Boolean, default=True)
    cutting_top = Column(Integer, default=0)
    stitches = Column(Integer, default=0)
    stacks = Column(Integer, default=0)
    batches = Column(Integer, default=0)
    cover_cutting_top = Column(Integer, default=0)
    cover_edge = Column(Integer, default=0)
    cover_thickness = Column(Integer, default=0)
    signature_pages = Column(Integer, default=0)
    signature_top_to_bottom = Column(Integer, default=0)
    signature_cutting_top = Column(Integer, default=0)
    signature_cutting_bottom = Column(Integer, default=0)
    signature_edge = Column(Integer, default=0)
    signature_thickness = Column(Integer, default=0)
    created_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
    updated_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
