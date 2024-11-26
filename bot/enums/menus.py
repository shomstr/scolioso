from enum import StrEnum, Enum
import re


class Emoji(StrEnum):
    WATER = "💧"
    PETALS = "🍃"
    TREE = "🌳"


class MainMenu(StrEnum):
    WALK = "Прогулка"
    WATERING = "🚿 Полить"
    BAG = "🎅 Садовник"


class MainMenuVars(Enum):
    WALK = [MainMenu.WALK.lower(), "прогулка", "гулять", "погулять"]
    WATERING = [MainMenu.WATERING.lower(), "полив", "полить"]
    BAG = [MainMenu.BAG.lower(), "садовник", f"{Emoji.TREE} Дерево".lower(), "дерево"]
    SMOKING = ["хапнуть", "скурить", "хап"]
    KEYBOARD = ["клава", "клавиатура", "+клава", "+кл", "кл", "+клавиатура", "+кнопки" "кнопки"]


re_keyboard = re.compile(r"клава|клавиатура|\+клава|\+кл|\+клавиатура|\+кнопки|кнопки|кл", re.IGNORECASE)
re_help = re.compile(r"(помощь|хелп)", re.IGNORECASE)
