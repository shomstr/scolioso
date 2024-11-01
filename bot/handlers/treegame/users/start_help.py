import logging

from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from bot.database.engine import Repositories
from bot.database.models import User
from bot.keyboards.default import main_menu
from bot.utils.texts import Texts

router = Router(name=__name__)
logger = logging.getLogger()


@router.message(CommandStart(), flags={"user": False, "chat": False})
async def start(message: types.Message) -> None:
    await message.reply(Texts.gettext("START"), reply_markup=main_menu)


@router.message(Command("help"))
async def help(message: types.Message, user: User, repo: Repositories) -> None:
    await message.reply(Texts.gettext("HELP"))
