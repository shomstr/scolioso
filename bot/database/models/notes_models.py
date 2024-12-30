from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, BIGINT, TEXT
from sqlalchemy.orm import mapped_column, Mapped
from .base_models import Base

if TYPE_CHECKING:
    pass

class Notes(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    note_id: Mapped[int] = mapped_column(BIGINT, default=0)

    title: Mapped[str] = mapped_column(TEXT, nullable=False)
    note_text: Mapped[str] = mapped_column(TEXT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())