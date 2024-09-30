from enum import StrEnum, Enum


class Emoji(StrEnum):
    WATER = "💧"
    PETALS = "🍃"
    TREE = "🌳"


class MainMenu(StrEnum):
    WALK = "Прогулка"
    WATERING = "🚿 Полить"
    BAG = "👨🏻‍🌾 Садовник"


class MainMenuVars(Enum):
    WALK = [MainMenu.WALK.lower(), "прогулка", "гулять"]
    WATERING = [MainMenu.WATERING, "полив", "полить"]
    BAG = [MainMenu.BAG.lower(), "садовник", f"{Emoji.TREE} Дерево".lower(), "дерево"]
