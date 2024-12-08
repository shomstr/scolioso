import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.enums.chat_type import ChatType
from aiogram.types import Message

from bot.keyboards.inline import start_keyboard_inline
from bot.utils.texts import Texts

router = Router(name=__name__)
logger = logging.getLogger()


@router.message(CommandStart(ignore_case=True), F.chat.type == ChatType.PRIVATE)
async def example_usage(msg: Message):
    await msg.answer(Texts.gettext("START"), reply_markup=start_keyboard_inline())
