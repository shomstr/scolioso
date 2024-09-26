import logging
import random
from datetime import datetime
from typing import Any

from aiogram import Router, F
from aiogram.types import Message
from asyncpg.pgproto.pgproto import timedelta

from bot.database.models import User
from bot.enums.menus import MainMenu
from bot.messages import BAG_TEXT, WALK_TEXTS, WATERING_TEXTS
from bot.utils.tree import formatted_heght_tree, formatted_next_walk

router = Router()
logger = logging.getLogger()


@router.message(F.text == MainMenu.BAG)
async def bag(message: Message, user: User):
    text = BAG_TEXT.format(
        user=user, tree=formatted_heght_tree(user.len_tree), watering_time=formatted_next_walk(user.last_walk)
    )
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


@router.message(F.text == MainMenu.WATERING)
async def watering(message: Message, user: User) -> Any:
    if user.water <= 0:
        return await message.reply("У вас нет воды для полива")
    heigth = random.randint(1, 5)

    user.len_tree += heigth
    user.water -= 1

    t = random.choice(WATERING_TEXTS)
    text = t.format(tree=formatted_heght_tree(heigth))

    await message.reply(text)
    return None
