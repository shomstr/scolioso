from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import BaseModel
from ...utils.links import get_openmessage_link, get_ping_link

if TYPE_CHECKING:
    from .chat import ChatUser


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(32), nullable=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)

    petals: Mapped[int] = mapped_column(Integer, server_default="0")
    water: Mapped[int] = mapped_column(Integer, server_default="0")
    len_tree: Mapped[int] = mapped_column(Integer, server_default="0")

    last_walk: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    chats_users: Mapped[list["ChatUser"]] = relationship("ChatUser", uselist=True, back_populates="user")

    vip_to: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())

    def ping_link(self) -> str:
        return get_ping_link(self.id, self.name)

    def openmessage_link(self) -> str:
        return get_openmessage_link(self.id, self.name)
