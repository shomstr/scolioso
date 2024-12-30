from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.dispatcher.flags import get_flag
from aiogram.enums import ChatType

from bot.database import get_repo
from bot.database.models import User

if TYPE_CHECKING:
    from aiogram.types import TelegramObject

    from bot.database.engine import Repositories

_IGNORED_NAMES = ["Group", "Channel"]

logger = logging.getLogger("DatabaseMiddleware")


class GetRepo(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        us = data["event_from_user"]

        if us.first_name in _IGNORED_NAMES:
            return

        async with get_repo() as repo:
            data["repo"] = repo

            await handler(event, data)


class GetUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        us = data["event_from_user"]

        if us.first_name in _IGNORED_NAMES:
            return None

        repo: Repositories = data["repo"]

        user_options = get_flag(data, "user_options", default=[])
        user = await repo.users.get(us.id, *user_options)

        data["is_new_user"] = False
        if not user:
            user: User = await repo.users.create(
                id=us.id, name=us.full_name, username=us.username
            )
            logger.info(f"Новый пользователь: {user.openmessage_link}")
            data["is_new_user"] = True
        data["user"] = user

        await handler(event, data)

        user.username = us.username.lower() if us.username else None
        user.name = us.full_name
        await repo.users.update(user)
        return None


class GetChat(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        _chat = data["event_chat"]

        if _chat.type == ChatType.PRIVATE:
            data["chat"] = None
            return await handler(event, data)

        repo: Repositories = data["repo"]

        chat_options = get_flag(data, "chat_options", default=[])

        chat = await repo.chats.get_by_chat_id(_chat.id, *chat_options)

        if not chat:
            chat = await repo.chats.create_from_aiogram_model(_chat)

        data["chat"] = chat

        await handler(event, data)

        chat.name = _chat.title
        chat.in_chat = True

        return None


class GetChatUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        chat = data["event_chat"]

        if chat.type == ChatType.PRIVATE:
            data["chat_user"] = None
            return await handler(event, data)

        repo: Repositories = data["repo"]

        chat_user_options = get_flag(data, "chat_user_options", default=[])

        chat_user = await repo.chats_users.get_chat_user(
            user.id, chat.id, *chat_user_options
        )
        if not chat_user:
            chat_user = await repo.chats_users.create_from_aiogram_model(user, chat)

        data["chat_user"] = chat_user

        await handler(event, data)
        await repo.chats_users.update(chat_user)
        return None


def setup_get_repo_middleware(dp: Dispatcher):
    """
    Setup GetRepo middleware for handlers
    :param dp:
    :return:
    """

    # default updates
    dp.message.middleware.register(GetRepo())
    dp.callback_query.middleware.register(GetRepo())
    dp.inline_query.middleware.register(GetRepo())

    # chats
    dp.my_chat_member.middleware.register(GetRepo())
    dp.chat_member.middleware.register(GetRepo())


def setup_get_user_middleware(dp: Dispatcher):
    """
    Setup GetUser middleware for handlers

    :param dp:
    :return:
    """

    dp.message.middleware.register(GetUser())
    dp.callback_query.middleware.register(GetUser())
    dp.inline_query.middleware.register(GetUser())

    # chats
    dp.my_chat_member.middleware.register(GetUser())
    dp.chat_member.middleware.register(GetUser())


def setup_get_chat_middleware(dp: Dispatcher):
    """
    Setup GetChat middleware for handlers

    :param dp:
    :return:
    """

    dp.message.middleware.register(GetChat())
    dp.callback_query.middleware.register(GetChat())
    dp.inline_query.middleware.register(GetChat())

    # chats
    dp.my_chat_member.middleware.register(GetChat())
    dp.chat_member.middleware.register(GetChat())


def setup_get_chat_user_middleware(dp: Dispatcher):
    """
    Setup GetChat middleware for handlers

    :param dp:
    :return:
    """

    dp.message.middleware.register(GetChatUser())
    dp.callback_query.middleware.register(GetChatUser())
    dp.inline_query.middleware.register(GetChatUser())

    # chats
    dp.my_chat_member.middleware.register(GetChatUser())
    dp.chat_member.middleware.register(GetChatUser())
