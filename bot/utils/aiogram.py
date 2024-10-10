import asyncio
import contextlib
import logging

from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InputFile

from bot.config import bot
from bot.database import Repositories
from bot.database.models import User


async def edit_message(
    message: Message, text: str, reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None
) -> Message:
    with contextlib.suppress(TelegramBadRequest):
        if message.photo:
            return await message.edit_caption(caption=text, reply_markup=reply_markup)
        return await message.edit_text(text=text, reply_markup=reply_markup)


async def get_user_by_username(repo: Repositories, username: str, *user_options) -> User | None:
    username = username.replace("@", "").lower()

    users = await repo.users.get_users_by_username(username, *user_options)

    if not users:
        return None

    for user in users:
        with contextlib.suppress(TelegramBadRequest):
            us = await bot.get_chat(user.id)
            current_username = us.username.lower() if us.username else None

            if username == current_username:
                return user

    else:
        return None


def get_user_from_message(message: Message, command: str | None = None) -> dict | None:
    text = message.text.lower()
    if command:
        text = text.replace(command, "")

    for i in text.split():
        if i.startswith("@"):
            if i[1:].isdigit():
                return {"user_id": int(i[1:])}  # Только user_id
            return {"username": i[1:]}  # Только username

    else:
        if message.reply_to_message:
            return {"user_id": message.reply_to_message.from_user.id}
        return None


async def send_message(
    chat_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None,
    photo: InputFile | str | None = None,
):
    with contextlib.suppress(TelegramForbiddenError, TelegramBadRequest):
        if photo:
            await bot.send_photo(chat_id, photo, reply_markup=reply_markup)
            return
        await bot.send_message(chat_id, text, reply_markup=reply_markup)


async def send_messages(
    users: list[int],
    text: str,
    from_message: Message | None = None,
    photo: str | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
):
    logger = logging.getLogger("mailing")
    a = [5, 15, 30, 60, 100, 150, 200, 300, 500, 750, 1000]
    all_users = 0

    for i, user in enumerate(users, start=1):
        try:
            if photo:
                await bot.send_photo(user, photo, text, eply_markup=reply_markup)
            else:
                await bot.send_message(user, text, reply_markup=reply_markup)

            if i in a:
                if from_message:
                    await from_message.message.answer(f"Было отправлено {i} юзерам")

            all_users += 1

        except (TelegramForbiddenError, TelegramBadRequest):
            pass

        except Exception:
            logger.error("Error", exc_info=True)

        await asyncio.sleep(0.3)

    else:
        if from_message:
            await from_message.answer(f"Всего было отправлено {all_users} из {len(users)}")

        logger.info(f"Всего было отправлено {all_users} из {len(users)}")
