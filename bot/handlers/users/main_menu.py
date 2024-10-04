import logging
import random
from datetime import datetime, timedelta
from typing import Any

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.types import Message

from bot.database import Repositories
from bot.database.models import User, ChatUser
from bot.enums.menus import MainMenuVars
from bot.filters import StartsWith
from bot.messages import (
    WALK_TEXTS,
    WATERING_TEXTS,
)
from bot.utils.aiogram import get_user_from_message, get_user_by_username
from bot.utils.texts import Texts
from bot.utils.tree import formatted_heght_tree, formatted_next_walk, walk_time

router = Router()
logger = logging.getLogger()


@router.message(StartsWith(MainMenuVars.BAG.value))
async def bag(message: Message, repo: Repositories, user: User, chat_user: ChatUser):
    us = get_user_from_message(message)
    if not us:
        is_self = True

    else:
        if us.get("user_id"):
            user = await repo.users.get(us.get("user_id"))
            if not user:
                return await message.reply("Юзер не найден")
        else:
            user = await get_user_by_username(repo, us.get("username"))
            if not user:
                return await message.reply("Юзер не найден")

        if message.chat.type == ChatType.PRIVATE:
            chat_user = None
        else:
            chat_user = await repo.chats_users.get_chat_user(
                user.id,
                message.chat.id,
            )

        is_self = False

    text = Texts.gettext(
        "BAG_TEXTS",
        context={
            "is_self": is_self,
            "user": user,
            "chat_user": chat_user,
            "tree": formatted_heght_tree(user.len_tree),
            "next_walk": formatted_next_walk(user),
            "walk_time": walk_time(user),
        },
    )
    await message.reply(text)
    return None


@router.message(StartsWith(MainMenuVars.WALK.value))
async def walk(message: Message, user: User, chat_user: ChatUser) -> Any:
    if user.last_walk and user.last_walk + timedelta(hours=walk_time(user)) > datetime.now():
        return await message.reply(f"Еще рано, {formatted_next_walk(user)}")

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
