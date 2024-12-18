from enum import Enum


class MessageCommands(Enum):
    GIVE_APPLE = ["/give_apple", "give_apples", "выдать яблоки", "выдать яблоко", "выдать мандарин", "выдать мандарины"]
    GIVE_WATER = [
        "/give_water",
        "выдать воды",
        "выдать воду",
    ]
    ADMIN_PANEL = ["юзеры", "бот инфо"]
