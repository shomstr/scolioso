import logging

from aiogram import Router, types, F

from bot.keyboards.default import main_menu
from bot.utils.texts import Texts

router = Router(name=__name__)
logger = logging.getLogger()


@router.callback_query(F.data == "start_game")
async def start_inline(call: types.CallbackQuery):
    await call.message.answer(Texts.gettext("START_GAME"), reply_markup=main_menu)
