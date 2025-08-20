import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.enums.chat_type import ChatType
from aiogram.types import Message
from bot.database.models import User, ChatUser, Chat
from bot.database.repos import Repositories

from bot.keyboards.inline import start_keyboard_inline
from bot.utils.aiogram import get_user_by_username, send_message

from bot.utils.texts import Texts

router = Router(name=__name__)
logger = logging.getLogger()


@router.message(CommandStart(ignore_case=True), F.chat.type == ChatType.PRIVATE)
async def example_usage(msg: Message,user: User, chat_user: ChatUser, repo: Repositories, us: dict | None = None):
    if not us:
        is_self = True


    text = Texts.gettext(
        "START",
        context={
            "is_self": is_self,
            "user": user
        },
    )
    await msg.reply(text, reply_markup=start_keyboard_inline())
    return None


