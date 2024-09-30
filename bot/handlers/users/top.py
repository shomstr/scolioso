import logging

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.types import Message

from bot.database import Repositories
from bot.enums.top import ChatTop, GlobalTop
from bot.filters import StartsWith
from bot.utils.tree import formatted_heght_tree, formatted_top_number

router = Router()
logger = logging.getLogger()


@router.message(StartsWith(GlobalTop.GLOBAL_TOP.value))
async def global_top(message: Message, repo: Repositories):
    top_users = await repo.users.top_users()
    text = "🌳Статистика деревьев мира: \n"

    for i, user in enumerate(top_users, start=1):
        text += f"{formatted_top_number(i)} {user.openmessage_link} - {formatted_heght_tree(user.len_tree)} \n"

    await message.reply(text)


@router.message(StartsWith(ChatTop.CHAT_TOP.value))
async def chat_top(message: Message, repo: Repositories):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("Работает только в чатах")

    top_users = await repo.chats_users.top_users(message.chat.id)

    text = "🌳Статистика деревьев группы: \n"

    for i, user in enumerate(top_users, start=1):
        text += f"{formatted_top_number(i)} {user.openmessage_link} - {formatted_heght_tree(user.len_tree)} \n"

    await message.reply(text)
    return None
