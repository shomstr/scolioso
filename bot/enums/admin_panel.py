from enum import Enum


class MessageCommands(Enum):
    GIVE_APPLE = ["/give_apple", "give_apples", "выдать яблоки", "выдать яблоко", "+яблоки", "+яблоки"]
    GIVE_WATER = ["/give_water", "выдать воды", "выдать воду", "+вода"]
