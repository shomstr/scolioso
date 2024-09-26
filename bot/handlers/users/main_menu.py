import logging

from aiogram import Router, F
from aiogram.types import Message

from bot.database.models import User
from bot.enums.menus import MainMenu
from bot.messages import BAG_TEXT

router = Router()
logger = logging.getLogger()


@router.message(F.text == MainMenu.BAG)
async def bag(message: Message, user: User):
    text = BAG_TEXT.format(user=user)
    await message.reply(text)
