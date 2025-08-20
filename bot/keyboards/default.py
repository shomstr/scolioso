from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.enums.menus import MainMenu


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=MainMenu.WALK), KeyboardButton(text=MainMenu.WATERING)],
        [KeyboardButton(text=MainMenu.BAG)],
    ],
    resize_keyboard=True,
    selective=True,
)


main2_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мужской'), KeyboardButton(text='Женский')],
        
    ],
    resize_keyboard=True,
    selective=True,
)