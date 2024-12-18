from __future__ import annotations

from typing import Sequence

from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload, InstrumentedAttribute

from .base import BaseRepo
from bot.database.models import User


class UsersRepo(BaseRepo):
    model = User

    async def get_by_user_id(self, user_id: int, *user_options) -> User | None:
        q = (
            select(User)
            .where(User.id == user_id)
            .options(*[selectinload(i) for i in user_options])
        )

        return (await self.session.execute(q)).scalar()

    async def get_users_by_username(
        self, username: str, *user_options
    ) -> Sequence[User]:
        q = (
            select(User)
            .where(User.username == username)
            .options(*[selectinload(i) for i in user_options])
        )

        return (await self.session.execute(q)).scalars().all()

    async def top_users(
        self, order_by: InstrumentedAttribute, limit=50
    ) -> Sequence[User]:
        q = select(User).where(order_by != 0).order_by(desc(order_by)).limit(limit)

        return (await self.session.execute(q)).scalars().all()

    async def get_all_users(self) -> Sequence[User]:
        q = select(User) 
        return (await self.session.execute(q)).scalars().all() 