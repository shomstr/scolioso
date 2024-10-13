import logging

from aiogram import Router, Bot
from aiogram.enums import ChatType
from aiogram.types import Message

from bot.database import Repositories
from bot.database.models import User, ChatUser, Chat
from bot.enums.top import ChatTop, GlobalTop
from bot.filters import Fullmatch
from bot.utils.texts import Texts

router = Router()
logger = logging.getLogger()


@router.message(Fullmatch(*GlobalTop.GLOBAL_TOP.value))
async def global_top(message: Message, repo: Repositories):
    users = await repo.users.top_users()
    text = Texts.gettext("TOP_USERS_GLOBAL", context={"users": users})

    await message.reply(text, parse_mode="HTML")


@router.message(Fullmatch(*ChatTop.CHAT_TOP.value))
async def chat_top(message: Message, repo: Repositories, chat: Chat, bot: Bot):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("Работает только в чатах")

    users = await repo.chats_users.top_users(message.chat.id, User.len_tree)

    text = Texts.gettext("TOP_USERS_CHAT", context={"users": users, "chat": chat})

    await message.reply(text)
    return None


@router.message(Fullmatch(*ChatTop.CHAT_TOP_DONATE.value))
async def chat_top_donate(message: Message, repo: Repositories, chat: Chat, bot: Bot):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("Работает только в чатах")
    users = await repo.chats_users.top_users(message.chat.id, ChatUser.foliage_chat_donate)
    text = Texts.gettext("TOP_USERS_CHAT_DONATE", context={"users": users, "chat": chat})

    await message.reply(text)
    return None
