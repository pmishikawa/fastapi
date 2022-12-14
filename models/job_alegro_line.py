from sqlalchemy import Column, Integer, String
from sqlalchemy.types import TIMESTAMP
from datetime import datetime, timedelta, timezone
from database import Base

JST = timezone(timedelta(hours=+9), "JST")


class JobAlegroLine(Base):
    __tablename__ = "job_alegro_line"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_job = Column(type_=TIMESTAMP(timezone=True))
    title = Column(String(255), default="")
    copies = Column(Integer, default=0)
    speed = Column(Integer, default=0)
    finished_top_to_bottom = Column(Integer, default=0)
    finished_edge = Column(Integer, default=0)
    cover_cutting_top = Column(Integer, default=0)
    cover_edge = Column(Integer, default=0)
    cover_thickness = Column(Integer, default=0)
    signature_cutting_top = Column(Integer, default=0)
    signature_edge = Column(Integer, default=0)
    signature_thickness = Column(Integer, default=0)
    created_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
    updated_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
