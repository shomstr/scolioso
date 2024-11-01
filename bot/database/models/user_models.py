from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base
from .types import integer
from ...utils.links import get_openmessage_link, get_ping_link

if TYPE_CHECKING:
    pass


class User(Base):
    __tablename__ = "users"
    _repr_attrs = ["id", "name"]

    name: Mapped[str] = mapped_column(String(128), nullable=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)

    petals: Mapped[integer]
    apples: Mapped[integer]
    water: Mapped[integer]
    len_tree: Mapped[integer]

    last_walk: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    vip_to: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())

    all_smokings: Mapped[integer]

    @property
    def ping_link(self) -> str:
        return get_ping_link(self.id, self.name)

    @property
    def openmessage_link(self) -> str:
        return get_openmessage_link(self.id, self.name)
