from sqlalchemy import Column, Integer, String
from sqlalchemy.types import TIMESTAMP
from datetime import datetime, timedelta, timezone
from database import Base

JST = timezone(timedelta(hours=+9), "JST")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(
        type_=TIMESTAMP(timezone=True), server_default=datetime.now(JST), nullable=False
    )
    updated_at = Column(
        type_=TIMESTAMP(timezone=True), default=datetime.now(JST), nullable=False
    )
