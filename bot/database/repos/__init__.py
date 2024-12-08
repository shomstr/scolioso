from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from .chat import ChatsRepo, ChatsUsersRepo
from .users import UsersRepo


@dataclass
class Repositories:
    session: AsyncSession
    users: UsersRepo
    chats: ChatsRepo
    chats_users: ChatsUsersRepo

    @staticmethod
    def get_repo(session: AsyncSession) -> Repositories:
        return Repositories(
            session=session,
            users=UsersRepo(session),
            chats=ChatsRepo(session),
            chats_users=ChatsUsersRepo(session),
        )


__all__ = [
    "Repositories",
]
