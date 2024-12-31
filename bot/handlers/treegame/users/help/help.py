import logging

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums.chat_type import ChatType
from aiogram.types import Message

from bot.utils.tree import (
    formatted_heght_tree,
    formatted_next_walk,
    walk_time,
)
from bot.database.models import User, ChatUser
from bot.enums import menus
from bot.database.engine import Repositories
from bot.keyboards.default import main_menu
from bot.keyboards.inline import main_keyboard_inline, help_keyboard
from bot.utils.texts import Texts

router = Router(name=__name__)
logger = logging.getLogger()


@router.message(CommandStart(deep_link=True))
@router.message(Command("help"))
@router.message(F.text.regexp(menus.re_help, mode="fullmatch"))
async def help(msg: types.Message, user: User, repo: Repositories) -> None:
    if msg.chat.type == ChatType.PRIVATE:
        return await msg.reply(Texts.gettext("HELP"), reply_markup=help_keyboard())

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
        if not us:
            is_self = True

        else:
            if us.get("user_id"):
                user = await repo.users.get(us.get("user_id"))
                if not user:
                    return await message.answer("Юзер не найден")
            else:
                user = await get_user_by_username(repo, us.get("username"))
                if not user:
                    return await message.answer("Юзер не найден")

            if message.chat.type == ChatType.PRIVATE:
                chat_user = None
            else:
                chat_user = await repo.chats_users.get_chat_user(
                    user.id,
                    message.chat.id,
                )

            is_self = False

        text = Texts.gettext(
            "SHORT_BAG_TEXTS",
            context={
                "is_self": is_self,
                "user": user,
                "chat_user": chat_user,
                "tree": formatted_heght_tree(user.len_tree)
            },
        )
        await msg.answer(
            text=text, reply_markup=main_keyboard_inline(id=msg.from_user.id)
        )
        return

    await msg.answer(
        Texts.gettext("KB_INFO_PRIVATE", context={"user": user}), reply_markup=main_menu
    )
