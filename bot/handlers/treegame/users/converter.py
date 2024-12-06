import logging
from typing import Any

from aiogram import Router
from aiogram.types import Message

from bot.config import WATER_TO_APPLE, APPLE_TO_WATER
from bot.database.models import User
from bot.filters import FullmatchWithArgs

router = Router()
logger = logging.getLogger()


@router.message(FullmatchWithArgs("купить мандарин", "купить мандарины", user=False))
async def buy_apple(message: Message, user: User, count: int) -> Any:
    if user.water < WATER_TO_APPLE * count:
        return await message.reply("Недостаточно воды для покупки")

    user.water -= WATER_TO_APPLE * count
    user.apples += count

    await message.reply(f"Вы купили {count} 🍊  за {WATER_TO_APPLE * count} 💧")
    return None


@router.message(FullmatchWithArgs("купить воду", "купить воды", user=False))
async def buy_water(message: Message, user: User, count: int) -> Any:
    if user.apples < APPLE_TO_WATER * count:
        return await message.reply("Недостаточно яблок для покупки")

    user.apples -= count
    user.water += WATER_TO_APPLE * count

    await message.reply(f"Вы купили {WATER_TO_APPLE * count} 💧 за {count} 🍏 ")
    return None
