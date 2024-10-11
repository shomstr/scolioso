import logging
import random
from datetime import datetime, timedelta
from typing import Any

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.types import Message
from aiogram.filters import or_f

from bot.config import MIN_LENGHT_TREE, MAX_LENGHT_TREE, MIN_PETALS_WALK, MIN_WATER_WALK, MAX_PETALS_WALK, MAX_WATER_WALK
from bot.database import Repositories
from bot.database.models import User, ChatUser, Chat
from bot.enums.menus import MainMenuVars
from bot.filters import StartsWith, Fullmatch
from bot.messages import (
    WALK_TEXTS,
    WATERING_TEXTS,
    SMOKING_TEXTS,
    CHAT_DONATE,
)
from bot.utils.aiogram import get_user_by_username
from bot.utils.texts import Texts
from bot.utils.tree import formatted_heght_tree, formatted_next_walk, walk_time

router = Router()
logger = logging.getLogger()


@router.message(
    or_f(Fullmatch(*MainMenuVars.BAG.value, count=False), Fullmatch(*MainMenuVars.BAG.value, user=False, count=False))
)
async def bag(
    message: Message,
    repo: Repositories,
    user: User,
    chat_user: ChatUser,
    us: dict | None,
):
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
    petals = random.randint(MIN_PETALS_WALK, MAX_PETALS_WALK)
    water = random.randint(MIN_WATER_WALK, MAX_WATER_WALK)
    user.petals += petals
    user.water += water

    if chat_user:
        chat_user.walks += 1

    t = random.choice(WALK_TEXTS)
    text = t.format(petals=petals, water=water)

    await message.reply(text)
    return None


@router.message(
    or_f(
        Fullmatch(*MainMenuVars.WATERING.value, user=False),
        Fullmatch(*MainMenuVars.WATERING.value, user=False, count=False),
    )
)
async def watering(message: Message, user: User, count: int | None) -> Any:
    count = count if count else 1
    if user.water < count:
        return await message.reply("У вас нет воды для полива")
    heigth = random.randint(MIN_LENGHT_TREE, MAX_LENGHT_TREE) * count

    user.len_tree += heigth
    user.water -= count

    t = random.choice(WATERING_TEXTS)
    text = t.format(tree=formatted_heght_tree(heigth), bottle=count)

    await message.reply(text)
    return None


@router.message(
    or_f(
        Fullmatch(*MainMenuVars.SMOKING.value, user=False),
        Fullmatch(*MainMenuVars.SMOKING.value, user=False, count=False),
    )
)
async def smoking(message: Message, user: User, count: int | None) -> Any:
    count = count if count else 1
    if user.petals < count:
        return await message.reply("Недостаточно листьев")

    user.petals -= count
    t = random.choice(SMOKING_TEXTS)
    text = t.format(user=user, count=count)
    await message.reply(text)
    return None


@router.message(
    Fullmatch("опад", user=False),
)
async def opad(message: Message, user: User, chat_user: ChatUser, chat: Chat, count: int) -> Any:
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("Работает только в чатах")

    if chat_user.foliage < count:
        return await message.reply("Недостаточно листвы")

    chat_user.foliage -= count
    chat.foliage += count

    t = CHAT_DONATE.format(user=user, chat=chat, count=count)
    await message.reply(t)
    return None
