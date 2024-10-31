from enum import Enum


class GlobalTop(list, Enum):
    GLOBAL_TOP = ["рейтинг мира", "рей мира", "топ мира"]
    GLOBAL_TOP_SMOKINGS = [
        *[f"{i} хап" for i in GLOBAL_TOP],
        *[f"{i} хапов" for i in GLOBAL_TOP],
    ]


class ChatTop(list, Enum):
    CHAT_TOP = ["рейтинг чата", "рей чата", "топ чата"]
    CHAT_TOP_DONATE = [f"{i} листвы" for i in CHAT_TOP]
    CHAT_TOP_SMOKING = [
        *[f"{i} хап" for i in CHAT_TOP],
        *[f"{i} хапов" for i in CHAT_TOP],
    ]
