from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_models import Base
from .mixins import UserRelationshipMixin
from .types import str_255, integer


class Chat(Base):
    __tablename__ = "chats"

    title: Mapped[str_255] = mapped_column(nullable=False)

    members: Mapped[list["ChatUser"]] = relationship(
        "ChatUser",
        foreign_keys="ChatUser.chat_id",
        back_populates="chat",
        uselist=True,
        passive_deletes=True,
        cascade="all, delete",
        post_update=True,
    )

    foliage: Mapped[integer]


class ChatUser(Base, UserRelationshipMixin):
    __tablename__ = "chats_users"
    _user_relationship_kwargs = {"lazy": "raise"}

    chat_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(Chat.id), nullable=False
    )
    chat: Mapped[Chat] = relationship(
        "Chat",
        uselist=False,
        foreign_keys=chat_id,
        remote_side="Chat.id",
        back_populates="members",
        lazy="raise",
    )

    foliage: Mapped[integer]
    foliage_chat_donate: Mapped[integer]
    walks: Mapped[integer]
