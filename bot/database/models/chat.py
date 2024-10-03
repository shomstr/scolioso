from __future__ import annotations


from sqlalchemy import String, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.models.base import Base

from bot.database.models import User


class Chat(Base):
    __tablename__ = "chats"

    title: Mapped[str] = mapped_column(String, nullable=False)

    members: Mapped[list["ChatUser"]] = relationship(
        "ChatUser",
        foreign_keys="ChatUser.chat_id",
        back_populates="chat",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete",
        post_update=True,
    )


class ChatUser(Base):
    __tablename__ = "chats_users"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(User.id), nullable=False)
    user: Mapped["User"] = relationship("User", uselist=False, foreign_keys=user_id, remote_side=User.id, lazy="raise")

    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Chat.id), nullable=False)
    chat: Mapped[Chat] = relationship(
        "Chat", uselist=False, foreign_keys=chat_id, remote_side="Chat.id", back_populates="members", lazy="raise"
    )

    foliage: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    walks: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
