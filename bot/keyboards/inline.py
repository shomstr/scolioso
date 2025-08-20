from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.utils.callback_factory.callback_factory import (
    next_data, prev_data,
    kl_tree_data, kl_walking_data,
    kl_watering_data
)

start_keyboard = InlineKeyboardBuilder(
    markup=[
        [
            InlineKeyboardButton(text="Bupyc", url="https://t.me/Not_Bupyc"),
            InlineKeyboardButton(
                text="Template", url="https://github.com/NotBupyc/aiogram-bot-template"
            ),
        ]
    ]
).as_markup()


def main_keyboard_inline(id: int):
    kb = InlineKeyboardBuilder()

    kb.button(text="Полить", callback_data=kl_watering_data(skill='watering_', id=id)),
    kb.button(text="Прогулка", callback_data=kl_walking_data(skill='walking_', id=id)),

    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def start_keyboard_inline():
    kb = InlineKeyboardBuilder()

    kb.button(text="☎️ Помощь", callback_data="help"),
    kb.button(text="➡️ Продолжить", callback_data="start_game")

    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def help_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(text="☎️ Помощь", callback_data="help"),
    kb.button(text="🆘️ Поддержка", callback_data="help_support")

    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def help_skip_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(text="Отмена", callback_data="support_cancel"),
    kb.button(text="Пропустить", callback_data="support_skip"),

    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def asdf():
    kb = InlineKeyboardBuilder()

    kb.button(text="❓️ Начать опрос", callback_data="start_opros")

    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def help_keyboard_inline(num: int):
    kb = InlineKeyboardBuilder()

    kb.button(text="⬅️", callback_data=prev_data(skill="help_prev_", num=num)),
    kb.button(text=f"{num}", callback_data="wed"),
    kb.button(text="➡️", callback_data=next_data(skill="help_next_", num=num))

    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
