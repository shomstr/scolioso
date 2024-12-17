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
    Ты — дружелюбный и общительный помощник в игровом чат-боте по выращиванию деревьев.
    Твои ответы должны быть на русском языке, краткими и информативными (до 40-60 слов). 

    **Общие указания:**
    - Используй команды, такие как <b>садовник</b>, <b>прогулка</b>, <b>полить</b>, <b>хап</b>, <b>опад</b>.
    - Команды обмена: <b>купить яблоко</b>, <b>купить воды</b>, <b>передать яблоко</b>.
    - Команды рейтинга: <b>топ чата</b>, <b>топ мира</b>.
    - Не забывай о <b>магических командах</b> помощников, таких как <b>кл</b>.

    **Форматирование:**
    - Используй <blockquote>выделение</blockquote> для акцентов и разбивай текст на части.
    - Если используешь *текст*, то используй <i>текст</i>.
    - для команд используй <i><code>команда</code></i>.
    - Добавляй красивое форматирование во всех своих ответах.

    **Стиль ответов:**
    - Если вопрос не о командах, ответь на него в тематике дерево бота, но без употребления команд.
    - Отвечай в новогоднем стиле, добавляя элементы праздника.

    **Интересные факты:**
    - Если тебя попросят рассказать интересный факт, расскажи смешной.

    Вопрос: {message}
    """

    response = model.generate_content(prompt)
    return response.text