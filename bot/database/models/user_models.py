from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, INTEGER, Float, TEXT
from sqlalchemy.orm import mapped_column, Mapped

from .base_models import Base
from .types import integer
from ...utils.links import get_openmessage_link, get_ping_link

if TYPE_CHECKING:
    pass


class User(Base):
    __tablename__ = "users"
    _repr_attrs = ["id", "name"]
    name: Mapped[str] = mapped_column(String(128), nullable=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)

    sex: Mapped[str] = mapped_column(String(15), nullable=True)
    age: Mapped[int] = mapped_column(INTEGER, nullable=True)

    ves: Mapped[float] = mapped_column(Float, nullable=True)
    rost: Mapped[float] = mapped_column(Float, nullable=True)

    zabol: Mapped[str] = mapped_column(String(10000), nullable=True)

    @property
    def ping_link(self) -> str:
        return get_ping_link(self.id, self.name)

    @property
    def openmessage_link(self) -> str:
        return get_openmessage_link(self.id, self.name)
