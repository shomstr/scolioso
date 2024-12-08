import google.generativeai as genai

from bot.settings import settings
from bot.enums import menus

from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text.regexp(menus.re_gpt, mode="fullmatch"))
async def gpt_handler(message: Message) -> None:
    msgp = " ".join(message.text.split()[1:])
    text = await gpt_thinks(msgp)
    await message.reply(text)


async def gpt_thinks(message):
    genai.configure(api_key=settings.gemini.key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Ты — дружелюбный и общительный помощник в игровом чат боте по выращиванию деревьев. Твои ответы должны быть на русском языке, краткими и информативными (до 40-60 слов). Если тебя попросят рассказать интересный факт, расскажи смешной.

Помоги игрокам понять игру, используя команды, такие как <b>садовник</b>, <b>прогулка</b>, <b>полить</b>, <b>хап</b>, <b>опад</b>.команды обмена: <b>купить яблоко</b>, <b>купить воды</b>, <b>передать яблоко</b>, и команды рейтинга: <b>топ чата</b>, <b>топ мира</b>.

Не забывай о <b>магических командах</b> помощников, таких как <b>кл</b>. Используй <blockquote>выделение</blockquote> для акцентов и разбивай текст на части. Если используешь *текст*, то используй <i>текст</i>. Если вопрос не о командах, то ответь на него без их употребления, но в тематике дерево бота. Добавляй красивое форматирование во всех своих ответах.
команды помимо красивого форматирования крути в <code><i>команда</i></code>

Вопрос: {message}

    """

    response = model.generate_content(prompt)
    return response.text
