from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
#from core.data.tricks.start_tricks import start_tricks as tricks

def main2_menu():
    kb = ReplyKeyboardBuilder()
    
    kb.button(text='Мужской'),
    kb.button(text='Женский'),
    
    kb.adjust(1),
    return kb.as_markup(resize_keyboard=True)