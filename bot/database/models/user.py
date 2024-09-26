from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = Column(String(32), nullable=True)

    petals: Mapped[int] = mapped_column(Integer, server_default="0")
    water: Mapped[int] = mapped_column(Integer, server_default="0")
    len_tree: Mapped[int] = mapped_column(Integer, server_default="0")

    last_walk: Mapped[datetime] = mapped_column(DateTime())
