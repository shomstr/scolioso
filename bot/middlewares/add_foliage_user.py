from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.enums import ChatType
from cachetools import TTLCache

from bot.database import get_repo

from aiogram.types import TelegramObject, User, Chat


logger = logging.getLogger("add_foliage")

ADD_FOLIAGE_KEY = "foliage-{user_id}-{chat_id}"


class AddFoliageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=60)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User = data["event_from_user"]
        chat: Chat = data["event_chat"]

        if chat.type == ChatType.PRIVATE:
            return await handler(event, data)

        key = ADD_FOLIAGE_KEY.format(user_id=user.id, chat_id=chat.id)

        if key in self.cache:
            return await handler(event, data)

        async with get_repo() as repo:
            if not await repo.users.get(user.id):
                return await handler(event, data)

            await repo.chats_users.add_foliage_in_chat(user.id, chat.id)

        logger.debug(f"Начислена листва для {user.full_name}")
        # await send_message(user.id, f"Вам начислена листва за общение в чате <b>{chat.title}</b>!")

        self.cache[key] = None
        return await handler(event, data)


def setup_add_foliage_middleware(dp: Dispatcher, rate_limit: float = 1.5):
    """
    Setup Throttling middleware for handlers

    :param rate_limit:
    :param dp:
    :return:
    """

    dp.message.outer_middleware.register(AddFoliageMiddleware())
