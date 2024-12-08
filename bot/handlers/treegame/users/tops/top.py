import logging

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import or_f
from aiogram.types import Message

from bot.database import Repositories
from bot.database.models import User, ChatUser, Chat
from bot.enums.top import ChatTop, GlobalTop
from bot.filters import Fullmatch, FullmatchWithArgs
from bot.utils.texts import Texts

router = Router()
logger = logging.getLogger()


# Топ деревьев
@router.message(
    or_f(
        FullmatchWithArgs(*GlobalTop.GLOBAL_TOP, user=False),
        Fullmatch(*GlobalTop.GLOBAL_TOP),
    )
)
async def global_top(message: Message, repo: Repositories, count: int = 50):
    if count > 100:
        count = 50

    users = await repo.users.top_users(User.len_tree, limit=count)
    text = Texts.gettext("TOP_USERS_GLOBAL", context={"users": users})

    await message.reply(text, parse_mode="HTML")


@router.message(
    or_f(FullmatchWithArgs(*ChatTop.CHAT_TOP, user=False), Fullmatch(*ChatTop.CHAT_TOP))
)
async def chat_top(message: Message, repo: Repositories, chat: Chat, count: int = 50):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("Работает только в чатах")

    if count > 100:
        count = 50

    users = await repo.chats_users.top_users(
        message.chat.id, User.len_tree, limit=count
    )
    text = Texts.gettext("TOP_USERS_CHAT", context={"users": users, "chat": chat})

    await message.reply(text)
    return None


@router.message(
    or_f(
        FullmatchWithArgs(*ChatTop.CHAT_TOP_DONATE, user=False),
        Fullmatch(*ChatTop.CHAT_TOP_DONATE),
    )
)
async def chat_top_donate(
    message: Message, repo: Repositories, chat: Chat, count: int = 50
):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("Работает только в чатах")

    if count > 100:
        count = 50

    users = await repo.chats_users.top_users(
        message.chat.id, ChatUser.foliage_chat_donate, limit=count
    )
    text = Texts.gettext(
        "TOP_USERS_CHAT_DONATE", context={"users": users, "chat": chat}
    )

    await message.reply(text)
    return None


@router.message(
    or_f(
        FullmatchWithArgs(*ChatTop.CHAT_TOP_SMOKING, user=False),
        Fullmatch(*ChatTop.CHAT_TOP_SMOKING),
    )
)
async def chat_top_smoking(
    message: Message, repo: Repositories, chat: Chat, count: int = 50
):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("Работает только в чатах")

    if count > 100:
        count = 50

    users = await repo.chats_users.top_users(
        message.chat.id, User.all_smokings, limit=count
    )
    text = Texts.gettext(
        "TOP_USERS_CHAT_SMOKINGS", context={"users": users, "chat": chat}
    )

    await message.reply(text)
    return None


@router.message(
    or_f(
        FullmatchWithArgs(*GlobalTop.GLOBAL_TOP_SMOKINGS, user=False),
        Fullmatch(*GlobalTop.GLOBAL_TOP_SMOKINGS),
    )
)
async def global_top_smoking(message: Message, repo: Repositories, count: int = 50):
    if count > 100:
        count = 50

    users = await repo.users.top_users(User.all_smokings, limit=count)
    text = Texts.gettext("TOP_USERS_GLOBAL_SMOKINGS", context={"users": users})

    await message.reply(text, parse_mode="HTML")
