from enum import StrEnum, Enum


class Emoji(StrEnum):
    WATER = "💧"
    PETALS = "🍃"
    TREE = "🌳"


class MainMenu(StrEnum):
    WALK = "Прогулка"
    WATERING = f"{Emoji.WATER} Полив"
    BAG = f"{Emoji.TREE} Дерево"


class MainMenuVars(Enum):
    WALK = [MainMenu.WALK.lower(), "прогулка", "гулять"]
    WATERING = [MainMenu.WATERING, "полив", "полить"]
    BAG = [MainMenu.BAG.lower(), "дерево"]
