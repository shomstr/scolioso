from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from .chat import ChatsRepo, ChatsUsersRepo
from .users import UsersRepo
from .notes import NotesRepo


@dataclass
class Repositories:
    session: AsyncSession
    users: UsersRepo
    chats: ChatsRepo
    chats_users: ChatsUsersRepo
    notes: NotesRepo

    @staticmethod
    def get_repo(session: AsyncSession) -> Repositories:
        return Repositories(
            session=session,
            users=UsersRepo(session),
            chats=ChatsRepo(session),
            chats_users=ChatsUsersRepo(session),
            notes=NotesRepo(session)
        )


__all__ = [
    "Repositories",
]
