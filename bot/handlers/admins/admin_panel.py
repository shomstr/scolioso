import logging
from typing import Any

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

from bot.database import Repositories
from bot.enums.admin_panel import MessageCommands
from bot.filters import IsAdmin, StartsWith
from bot.messages import BOT_INFO
from bot.utils.aiogram import get_user_by_username, get_user_from_message, send_message
from bot.utils.misc import bot_info_dict

router = Router()
logger = logging.getLogger(__name__)

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command("botinfo"))
async def bot_info(message: types.Message) -> None:
    text = BOT_INFO.format(**await bot_info_dict())
    await message.answer(text=text)


@router.message(StartsWith(MessageCommands.GIVE_APPLE.value))
async def give_apple(message: Message, repo: Repositories, command: str) -> Any:
    us = get_user_from_message(message, command)
    t = message.text.lower().replace(command, "")

    if not us:
        return await message.answer("Укажите юзера")

    if us.get("user_id"):
        user = await repo.users.get(us.get("user_id"))
        if not user:
            return await message.reply("Юзер не найден")
    else:
        user = await get_user_by_username(repo, us.get("username"))
        if not user:
            return await message.reply("Юзер не найден")

    apples = int(t.split()[1])

    user.apples += apples
    await repo.users.update(user)
    await message.reply(f"Вы выдали {apples} 🍎 {user.ping_link}")
    await send_message(user.id, f"Вам выдали {apples} 🍎")
    return None


@router.message(StartsWith(MessageCommands.GIVE_WATER.value))
async def give_water(message: Message, repo: Repositories, command: str) -> Any:
    us = get_user_from_message(message, command)
    t = message.text.lower().replace(command, "")

    if not us:
        return await message.answer("Укажите юзера")

    if us.get("user_id"):
        user = await repo.users.get(us.get("user_id"))
        if not user:
            return await message.reply("Юзер не найден")
    else:
        user = await get_user_by_username(repo, us.get("username"))
        if not user:
            return await message.reply("Юзер не найден")

    water = int(t.split()[1])

    user.water += water
    await repo.users.update(user)
    await message.reply(f"Вы выдали {water} 💧 {user.ping_link}")
    await send_message(user.id, f"Вам выдали {water} 💧")
    return None
