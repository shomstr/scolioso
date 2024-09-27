from __future__ import annotations

from sqlalchemy import String, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.models import User
from bot.database.models.base import BaseModel


class Chat(BaseModel):
    __tablename__ = "chats"

    title: Mapped[str] = mapped_column(String, nullable=False)

    members: Mapped["ChatUser"] = relationship(
        "ChatUser",
        foreign_keys="ChatUser.chat_id",
        back_populates="chat",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete",
        post_update=True,
    )


class ChatUser(BaseModel):
    __tablename__ = "chats_users"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(User.id), nullable=False)
    user: Mapped[User] = relationship(User, uselist=False, foreign_keys=user_id, remote_side=User.id)

    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Chat.id), nullable=False)
    chat: Mapped[Chat] = relationship(
        Chat, uselist=False, foreign_keys=chat_id, remote_side=Chat.id, back_populates="members"
    )

    foliage: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    walks: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
