import logging
from typing import Any

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

from bot.database import Repositories
from bot.enums.admin_panel import MessageCommands
from bot.filters import IsAdmin, FullmatchWithArgs
from bot.messages import BOT_INFO
from bot.utils.aiogram import get_user_by_username, send_message
from bot.utils.misc import bot_info_dict

router = Router()
logger = logging.getLogger(__name__)

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command("botinfo"))
async def bot_info(message: types.Message) -> None:
    text = BOT_INFO.format(**await bot_info_dict())
    await message.answer(text=text)


@router.message(FullmatchWithArgs(*MessageCommands.GIVE_APPLE.value))
async def give_apple(message: Message, repo: Repositories, us: dict | None, count: int) -> Any:
    if not us:
        return await message.answer("Укажите юзера")
    if count > 10_000:
        return await message.reply("Ограничение на выдачу 10000")

    if us.get("user_id"):
        user = await repo.users.get(us.get("user_id"))
        if not user:
            return await message.reply("Юзер не найден")
    else:
        user = await get_user_by_username(repo, us.get("username"))
        if not user:
            return await message.reply("Юзер не найден")

    user.apples += count
    await repo.users.update(user)

    await message.reply(f"Вы выдали {count} 🍎 {user.ping_link}")
    await send_message(user.id, f"Вам выдали {count} 🍎")

    return None


@router.message(FullmatchWithArgs(*MessageCommands.GIVE_WATER.value))
async def give_water(message: Message, repo: Repositories, us: dict | None, count: int) -> Any:
    if not us:
        return await message.answer("Укажите юзера")
    if count > 10_000:
        return await message.reply("Ограничение на выдачу 10_000")

    if us.get("user_id"):
        user = await repo.users.get(us.get("user_id"))
        if not user:
            return await message.reply("Юзер не найден")
    else:
        user = await get_user_by_username(repo, us.get("username"))
        if not user:
            return await message.reply("Юзер не найден")

    user.water += count
    await repo.users.update(user)

    await message.reply(f"Вы выдали {count} 💧 {user.ping_link}")
    await send_message(user.id, f"Вам выдали {count} 💧")

    return None
