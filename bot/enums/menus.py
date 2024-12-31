from enum import StrEnum, Enum
import re


class Emoji(StrEnum):
    WATER = "💧"
    PETALS = "🍃"
    TREE = "🌳"


class MainMenu(StrEnum):
    WALK = "Прогулка"
    WATERING = "🚿 Полить"
    BAG = "🎅 Дерево"


class MainMenuVars(Enum):
    WALK = [MainMenu.WALK.lower(), "прогулка", "гулять", "погулять"]
    WATERING = [MainMenu.WATERING.lower(), "полив", "полить"]
    BAG = [MainMenu.BAG.lower(), f"{Emoji.TREE} Дерево".lower(), "дерево", "елка".lower(), "ёлка".lower()]
    SMOKING = ["хапнуть", "скурить", "хап"]
    KEYBOARD = [
        "клава",
        "клавиатура",
        "+клава",
        "+кл",
        "кл",
        "+клавиатура",
        "+кнопки" "кнопки",
    ]


re_keyboard = re.compile(
    r"клава|клавиатура|\+клава|\+кл|\+клавиатура|\+кнопки|кнопки|кл", re.IGNORECASE
)
re_help = re.compile(r"(помощь|хелп)", re.IGNORECASE)
re_gpt = re.compile(r"дерево\s*(.*)", re.IGNORECASE)
re_gpt_2 = re.compile(r"древо\s*(.*)", re.IGNORECASE)

re_pref = r'([!./]|)'
re_add_note = re.compile(r'^\+ветка\s+([\s\S]+?)\n([\s\S]+)', re.IGNORECASE)
re_del_note = re.compile(r'^\-ветка\s+(.+?)', re.IGNORECASE)

re_show_note = re.compile(re_pref + r'^\ветка\s+(.+?)', re.IGNORECASE)
re_show_all_notes = re.compile(re_pref + r'^ветки', re.IGNORECASE)