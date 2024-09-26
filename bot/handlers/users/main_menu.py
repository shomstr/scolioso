import logging
import random
from datetime import datetime
from typing import Any

from aiogram import Router, F
from aiogram.types import Message
from asyncpg.pgproto.pgproto import timedelta

from bot.database.models import User
from bot.enums.menus import MainMenu
from bot.messages import BAG_TEXT, WALK_TEXTS

router = Router()
logger = logging.getLogger()


@router.message(F.text == MainMenu.BAG)
async def bag(message: Message, user: User):
    text = BAG_TEXT.format(user=user)
    await message.reply(text)


@router.message(F.text == MainMenu.WALK)
async def walk(message: Message, user: User) -> Any:
    if user.last_walk and user.last_walk + timedelta(hours=12) > datetime.now():
        return await message.answer("Еще рано для прогулки")

    user.last_walk = datetime.now()
    petals = random.randint(1, 10)
    water = random.randint(1, 5)
    user.petals += petals
    user.water += water

    t = random.choice(WALK_TEXTS)
    text = t.format(petals=petals, water=water)

    await message.reply(text)
    return None
