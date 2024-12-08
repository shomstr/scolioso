import logging

from aiogram import Router, types, F

from bot.database.engine import Repositories
from bot.keyboards.inline import help_keyboard_inline
from bot.utils.texts import Texts
from bot.utils.callback_factory.callback_factory import prev_data, next_data

router = Router(name=__name__)
logger = logging.getLogger()


@router.callback_query(F.data == "help")
async def help_inline(call: types.CallbackQuery):
    await call.message.edit_text(
        Texts.gettext("HELP"), reply_markup=help_keyboard_inline(num=0)
    )


@router.callback_query(prev_data.filter(F.skill.startswith("help_prev_")))
async def prev_help(
    call: types.CallbackQuery, repo: Repositories, callback_data: prev_data
):
    page = callback_data.num
    if page <= 0:
        return await call.answer("больше ничего нет")

    next_prev_page = page - 1

    await call.message.edit_text(
        Texts.gettext(f"HELP_{next_prev_page}"),
        reply_markup=help_keyboard_inline(num=next_prev_page),
    )
    return None


@router.callback_query(next_data.filter(F.skill.startswith("help_next_")))
async def next_help(
    call: types.CallbackQuery, repo: Repositories, callback_data: prev_data
):
    page = callback_data.num
    if page >= 4:
        return await call.answer("больше ничего нет")

    next_next_page = page + 1

    await call.message.edit_text(
        Texts.gettext(f"HELP_{next_next_page}"),
        reply_markup=help_keyboard_inline(num=next_next_page),
    )
    return None
