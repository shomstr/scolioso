from enum import StrEnum


class Emoji(StrEnum):
    WATER = "💧"
    PETALS = "🍃"
    TREE = "🌳"


class MainMenu(StrEnum):
    WALK = "Прогулка"
    WATERING = "Полив"
    BAG = f"{Emoji.TREE} Дерево"
