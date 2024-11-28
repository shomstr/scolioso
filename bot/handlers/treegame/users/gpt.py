import google.generativeai as genai
from bot.enums import menus
from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text.regexp(menus.re_gpt, mode="fullmatch"))
async def gpt_handler(message: Message) -> None:
    msgp = " ".join(message.text.split()[1:])
    text = gpt_thinks(msgp)
    await message.answer(text)
    await message.answer(msgp)


async def gpt_thinks(message):
    genai.configure(api_key="AIzaSyDGZTTmMaUtdkr5E8U9AAs_Wl2NfTJtFe0")
    model = genai.GenerativeModel("gemini-1.5-flash")
    text1 = message.text
    response = model.generate_content(text1)
    return response.text
