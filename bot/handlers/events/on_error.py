import logging
from typing import cast

from aiogram import Router
from aiogram.exceptions import TelegramRetryAfter
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Update, Message

router = Router()
logger = logging.getLogger(__name__)


@router.error(ExceptionTypeFilter(TelegramRetryAfter))
async def floodwait_error(event: ErrorEvent) -> None:
    update: Update = event.update
    retry_after = event.exception.retry_after

    if message := update.message:
        chat = message.chat
        chat_id = chat.id

    elif query := update.callback_query:
        message = cast(Message, query.message)

        chat = message.chat
        chat_id = chat.id

    elif update.inline_query:
        chat_id = None

    elif update.my_chat_member:
        chat_id = None

    elif chat_member := update.chat_member:
        chat = chat_member.chat
        chat_id = chat.id
    else:
        return

    logger.error(f"Флудвейт в чате {chat_id} на {retry_after} секунд")


@router.errors()
async def error_handler(exception: ErrorEvent) -> None:
    update: Update = exception.update

    if message := update.message:
        user = message.from_user
        chat = message.chat

        user_id = user.id if user else None
        user_full_name = user.full_name if user else None

        chat_id = chat.id

    elif query := update.callback_query:
        message = cast(Message, query.message)

        user = message.from_user if message.from_user else None
        chat = message.chat

        user_id = user.id if user else None
        user_full_name = user.full_name if user else None

        chat_id = chat.id

    elif inline := update.inline_query:
        user = inline.from_user

        user_id = user.id if user else None
        user_full_name = user.full_name if user else None

        chat_id = None

    elif my_chat := update.my_chat_member:
        user = my_chat.from_user

        user_id = user.id if user else None
        user_full_name = user.full_name if user else None

        chat_id = None

    elif chat_member := update.chat_member:
        user = chat_member.from_user
        chat = chat_member.chat
        user_id = user.id if user else None
        user_full_name = user.full_name if user else None

        chat_id = chat.id
    else:
        logger.warning("Unknow update, %s", exception.update)
        return

    logger.error(f"User={user_full_name} id={user_id} chat_id={chat_id if chat_id else 'No chat'}", exc_info=True)
