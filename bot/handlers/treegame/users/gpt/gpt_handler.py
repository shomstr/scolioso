
from bot.enums import menus
from bot.handlers.treegame.users.gpt.gpt import gpt_thinks, gpt_thinks_2
from aiogram import Router, F
from aiogram.types import Message
from bot.enums import menus

router = Router()


@router.message(F.text.regexp(menus.re_gpt, mode="fullmatch"))
async def gpt_handler(message: Message) -> None:
    msgp = " ".join(message.text.split()[1:])
    text = await gpt_thinks(msgp)
    await message.reply(text)

@router.message(F.text.regexp(menus.re_gpt_2, mode="fullmatch"))
async def gpt_handler(message: Message) -> None:
    msgp = " ".join(message.text.split()[1:])
    text = await gpt_thinks_2(msgp)
    await message.reply(text)
