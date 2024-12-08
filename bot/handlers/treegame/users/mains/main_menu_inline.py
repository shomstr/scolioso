import logging
import random
from datetime import datetime, timedelta
from typing import Any

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram import types

from bot.config import (
    MIN_LENGHT_TREE,
    MAX_LENGHT_TREE,
    MIN_PETALS_WALK,
    MIN_WATER_WALK,
    MAX_PETALS_WALK,
    MAX_WATER_WALK,
)
from bot.database import Repositories
from bot.database.models import User, ChatUser
from bot.messages import WALK_TEXTS, WATERING_TEXTS
from bot.utils.aiogram import get_user_by_username
from bot.utils.texts import Texts
from bot.utils.tree import (
    formatted_heght_tree,
    formatted_next_walk,
    walk_time,
    check_walk,
)

router = Router(name=__name__)
logger = logging.getLogger()


@router.callback_query(F.data == "water")
async def watering_callback(
    call: types.CallbackQuery,
    repo: Repositories,
    user: User,
    chat_user: ChatUser,
    count: int | None = None,
) -> Any:
    id = call.from_user.id

    user = await repo.users.get(id)
    if not user:
        return await call.answer("Юзер не найден")

    if call.message.chat.type == ChatType.PRIVATE:
        pass
    else:
        await repo.chats_users.get_chat_user(
            user.id,
            call.message.chat.id,
        )

    count = count if count else 1

    if user.water < count:
        return await call.answer("У вас нет воды для полива")

    height = random.randint(MIN_LENGHT_TREE, MAX_LENGHT_TREE) * count
    user.len_tree += height
    user.water -= count

    t = random.choice(WATERING_TEXTS)
    text = t.format(tree=formatted_heght_tree(height), bottle=count)

    await call.message.answer(text)
    return None


@router.callback_query(F.data == "walking")
async def walk_callback(
    call: types.CallbackQuery, repo: Repositories, user: User, chat_user: ChatUser
) -> Any:
    id = call.from_user.id

    user = await repo.users.get(id)
    if not user:
        return await call.answer("Юзер не найден")

    if call.message.chat.type == ChatType.PRIVATE:
        chat_user = None
    else:
        chat_user = await repo.chats_users.get_chat_user(
            user.id,
            call.message.chat.id,
        )

    if (
        user.last_walk
        and user.last_walk + timedelta(hours=walk_time(user)) > datetime.now()
    ):
        return await call.answer(f"Еще рано, {formatted_next_walk(user)}")

    user.last_walk = datetime.now()
    petals = random.randint(MIN_PETALS_WALK, MAX_PETALS_WALK)
    water = random.randint(MIN_WATER_WALK, MAX_WATER_WALK)
    user.petals += petals
    user.water += water

    if chat_user:
        chat_user.walks += 1

    t = random.choice(WALK_TEXTS)
    text = t.format(petals=petals, water=water)

    await call.message.answer(text)
    return None


@router.callback_query(F.data == "gardener")
async def gardener(
    call: types.CallbackQuery, repo: Repositories, user: User, chat_user: ChatUser
) -> Any:
    id = call.from_user.id

    user = await repo.users.get(id)
    if not user:
        return await call.answer("Юзер не найден")
    user = await get_user_by_username(repo, call.from_user.username)
    if not user:
        return await call.answer("Юзер не найден")

    if call.message.chat.type == ChatType.PRIVATE:
        chat_user = None
    else:
        chat_user = await repo.chats_users.get_chat_user(
            user.id,
            call.message.chat.id,
        )

    text = Texts.gettext(
        "BAG_TEXTS",
        context={
            "user": user,
            "chat_user": chat_user,
            "tree": formatted_heght_tree(user.len_tree),
            "next_walk": formatted_next_walk(user),
            "walk_time": walk_time(user),
            "check_walk": check_walk(user),
        },
    )
    await call.message.answer(text)
    return None
