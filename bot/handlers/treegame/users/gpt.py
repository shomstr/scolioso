import google.generativeai as genai

from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text.contains("дерево"))
async def gpt_handler(message: Message) -> None:
    message.text.split()[1:]
    text = await gpt_thinks(message)
    await message.answer(text)


async def gpt_thinks(message):
    genai.configure(api_key="AIzaSyDGZTTmMaUtdkr5E8U9AAs_Wl2NfTJtFe0")
    model = genai.GenerativeModel("gemini-1.5-flash")
    text1 = message.text
    response = model.generate_content(text1)
    return response.text
