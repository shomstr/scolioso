from __future__ import annotations


from sqlalchemy import String, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.models.base import Base

from bot.database.models.mixins import UserRelationshipMixin


class Chat(Base):
    __tablename__ = "chats"

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    members: Mapped[list["ChatUser"]] = relationship(
        "ChatUser",
        foreign_keys="ChatUser.chat_id",
        back_populates="chat",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete",
        post_update=True,
    )

    foliage: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")


class ChatUser(Base, UserRelationshipMixin):
    __tablename__ = "chats_users"
    _user_relationship_kwargs = {"lazy": "raise"}

    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Chat.id), nullable=False)
    chat: Mapped[Chat] = relationship(
        "Chat", uselist=False, foreign_keys=chat_id, remote_side="Chat.id", back_populates="members", lazy="raise"
    )

    foliage: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    foliage_chat_donate: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    walks: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
