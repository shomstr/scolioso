from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.utils.callback_factory.callback_factory import next_data, prev_data

start_keyboard = InlineKeyboardBuilder(
    markup=[
        [
            InlineKeyboardButton(text="Bupyc", url="https://t.me/Not_Bupyc"),
            InlineKeyboardButton(text="Template", url="https://github.com/NotBupyc/aiogram-bot-template"),
        ]
    ]
).as_markup()


def main_keyboard_inline():
    kb = InlineKeyboardBuilder()

    (kb.button(text="Полить", callback_data="water"),)
    (kb.button(text="Прогулка", callback_data="walking"),)
    (kb.button(text="Садовник", callback_data="gardener"),)

    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def start_keyboard_inline():
    kb = InlineKeyboardBuilder()

    (kb.button(text="☎️ Помощь", callback_data="help"),)
    (kb.button(text="🌲 Начать игру", callback_data="start_game"),)

    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def help_keyboard_inline(num: int):
    kb = InlineKeyboardBuilder()

    (kb.button(text="⬅️", callback_data=prev_data(skill="help_prev_", num=num)),)
    (kb.button(text=f"{num}", callback_data="wed"),)
    kb.button(text="➡️", callback_data=next_data(skill="help_next_", num=num))

    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
