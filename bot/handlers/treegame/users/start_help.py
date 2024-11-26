import logging

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums.chat_type import ChatType
from aiogram.types import Message
from bot.database.models import User, ChatUser
from bot.enums import menus
from bot.database.engine import Repositories
from bot.keyboards.default import main_menu
from bot.keyboards.inline import start_keyboard_inline, main_keyboard_inline
from bot.utils.texts import Texts

router = Router(name=__name__)
logger = logging.getLogger()


@router.message(CommandStart(ignore_case=True), F.chat.type == ChatType.PRIVATE)
async def example_usage(msg: Message):
    await msg.answer(Texts.gettext("START"), reply_markup=start_keyboard_inline())


@router.message(Command("help"))
@router.message(F.text.regexp(menus.re_help, mode="fullmatch"))
async def help(msg: types.Message, user: User, repo: Repositories) -> None:
    if msg.chat.type == ChatType.PRIVATE:
        return await msg.reply(Texts.gettext("HELP"))

    await msg.reply(Texts.gettext("HELP_CHAT"))
    return None


@router.message(F.text.regexp(menus.re_keyboard, mode="fullmatch"))
async def kb(
    msg: Message,
    repo: Repositories,
    user: User,
    chat_user: ChatUser,
    us: dict | None = None,
):
    if msg.chat.type != "private":
        await msg.answer(Texts.gettext("KB_INFO_CHAT"), reply_markup=main_keyboard_inline())
        return

    await msg.answer(Texts.gettext("KB_INFO_PRIVATE", context={"user": user}), reply_markup=main_menu)
