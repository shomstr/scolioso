import logging
import random
from datetime import datetime
from typing import Any

from aiogram import Router
from aiogram.types import Message
from asyncpg.pgproto.pgproto import timedelta

from bot.database import Repositories
from bot.database.models import User, ChatUser
from bot.enums.menus import MainMenuVars
from bot.filters import StartsWith
from bot.messages import (
    WALK_TEXTS,
    WATERING_TEXTS,
    YOUR_BAG_TEXT,
    YOUR_BAG_TEXT_IN_CHAT,
    OTHER_BAG_TEXT_IN_CHAT,
    OTHER_BAG_TEXT,
)
from bot.utils.aiogram import get_user_from_message, get_user_by_username
from bot.utils.tree import formatted_heght_tree, formatted_next_walk

router = Router()
logger = logging.getLogger()


@router.message(StartsWith(MainMenuVars.BAG.value))
async def bag(message: Message, repo: Repositories, user: User, chat_user: ChatUser):
    us = get_user_from_message(message)
    if not us:
        if chat_user:
            text = YOUR_BAG_TEXT_IN_CHAT.format(
                user=user,
                tree=formatted_heght_tree(user.len_tree),
                watering_time=formatted_next_walk(user.last_walk),
                chat_user=chat_user,
            )
        else:
            text = YOUR_BAG_TEXT.format(
                user=user,
                tree=formatted_heght_tree(user.len_tree),
                watering_time=formatted_next_walk(user.last_walk),
            )
    else:
        if us.get("user_id"):
            user = await repo.users.get(us.get("user_id"))
            chat_user = await repo.chats_users.get(us.get("user_id"))
        else:
            user = await get_user_by_username(repo, us.get("username"))
            if not user:
                return message.reply("Юзер не найден")
            chat_user = await repo.chats_users.get_chat_user(user.id, message.chat.id)

        if chat_user:
            text = OTHER_BAG_TEXT_IN_CHAT.format(
                user=user,
                tree=formatted_heght_tree(user.len_tree),
                watering_time=formatted_next_walk(user.last_walk),
                chat_user=chat_user,
            )
        else:
            text = OTHER_BAG_TEXT.format(
                user=user,
                tree=formatted_heght_tree(user.len_tree),
                watering_time=formatted_next_walk(user.last_walk),
            )

    await message.reply(text)
    return None


@router.message(StartsWith(MainMenuVars.WALK.value))
async def walk(message: Message, user: User, chat_user: ChatUser) -> Any:
    if user.last_walk and user.last_walk + timedelta(hours=0) > datetime.now():
        return await message.answer("Еще рано для прогулки")

    user.last_walk = datetime.now()
    petals = random.randint(1, 10)
    water = random.randint(1, 5)
    user.petals += petals
    user.water += water

    if chat_user:
        chat_user.walks += 1

    t = random.choice(WALK_TEXTS)
    text = t.format(petals=petals, water=water)

    await message.reply(text)
    return None


@router.message(StartsWith(MainMenuVars.WATERING.value))
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
