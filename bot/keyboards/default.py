from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.enums.menus import MainMenu


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=MainMenu.WALK), KeyboardButton(text=MainMenu.WATERING)],
        [KeyboardButton(text=MainMenu.BAG)],
    ],
    resize_keyboard=True,
    selective=True,
)
def main2_menu():
    kb = ReplyKeyboardBuilder()
    
    kb.button(text='Мужской'),
    kb.button(text='Женский'),
    
    kb.adjust(1),
    return kb.as_markup(resize_keyboard=True)