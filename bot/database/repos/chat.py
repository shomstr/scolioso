from __future__ import annotations

from typing import Sequence

from sqlalchemy import select, update, desc
from sqlalchemy.orm import selectinload, joinedload

from .base import BaseRepo
from bot.database.models import User, Chat, ChatUser
from aiogram.types import User as AiogramUser, Chat as AiogramChat


class ChatsRepo(BaseRepo):
    model = Chat

    async def get_by_chat_id(self, chat_id: int, *chat_options) -> User | None:
        q = select(Chat).where(Chat.id == chat_id).options(*[selectinload(i) for i in chat_options])

        return (await self.session.execute(q)).scalar()


class ChatsUsersRepo(BaseRepo):
    model = ChatUser

    async def get_chat_user(self, user_id: int, chat_id: int, *chat_options) -> ChatUser | None:
        q = (
            select(ChatUser)
            .where(ChatUser.user_id == user_id, ChatUser.chat_id == chat_id)
            .options(*[selectinload(i) for i in chat_options])
        )

        return (await self.session.execute(q)).scalar()

    async def create_from_aiogram_model(self, user: AiogramUser, chat: AiogramChat) -> ChatUser:
        us: User = ChatUser(user_id=user.id, chat_id=chat.id)
        await self.create_from_model(us)

        return us

    async def add_foliage_in_chat(self, user_id: int, chat_id: int, foliage: int = 1):
        q = (
            update(ChatUser)
            .where(
                ChatUser.user_id == user_id,
                ChatUser.chat_id == chat_id,
            )
            .values(foliage=ChatUser.foliage + foliage)
        )

        await self.session.execute(q)
        await self.session.commit()

    async def top_users(self, chat_id: int, order_by: str) -> Sequence[ChatUser]:
        q = (
            select(ChatUser)
            .join(User)
            .where(ChatUser.user_id == User.id, ChatUser.chat_id == chat_id, order_by != 0)
            .order_by(desc(order_by))
            .limit(50)
            .options(joinedload(ChatUser.user))
        )

        return (await self.session.execute(q)).scalars().all()
