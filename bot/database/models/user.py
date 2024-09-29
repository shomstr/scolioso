from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from .base import BaseModel
from ...utils.links import get_openmessage_link, get_ping_link


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(32), nullable=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)

    petals: Mapped[int] = mapped_column(Integer, server_default="0")
    water: Mapped[int] = mapped_column(Integer, server_default="0")
    len_tree: Mapped[int] = mapped_column(Integer, server_default="0")

    last_walk: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    @property
    def ping_link(self) -> str:
        return get_ping_link(self.id, self.name)

    @property
    def openmessage_link(self) -> str:
        return get_openmessage_link(self.id, self.name)
