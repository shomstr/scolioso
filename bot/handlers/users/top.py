import logging

from aiogram import Router, Bot
from aiogram.enums import ChatType
from aiogram.types import Message

from bot.database import Repositories
from bot.enums.top import ChatTop, GlobalTop
from bot.filters import StartsWith
from bot.utils.texts import Texts

router = Router()
logger = logging.getLogger()


@router.message(StartsWith(GlobalTop.GLOBAL_TOP.value))
async def global_top(message: Message, repo: Repositories):
    users = await repo.users.top_users()
    text = Texts.gettext("TOP_USERS_GLOBAL", context={"users": users})

    await message.reply(text, parse_mode="HTML")


@router.message(StartsWith(ChatTop.CHAT_TOP.value))
async def chat_top(message: Message, repo: Repositories, bot: Bot):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("Работает только в чатах")

    users = await repo.chats_users.top_users(message.chat.id)
    text = Texts.gettext("TOP_USERS_CHAT", context={"users": users, "chat": message.chat})

    await message.reply(text)
    return None
