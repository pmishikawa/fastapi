from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.types import TIMESTAMP
from datetime import datetime, timedelta, timezone
from database import Base


JST = timezone(timedelta(hours=+9), "JST")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    created_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
    updated_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
