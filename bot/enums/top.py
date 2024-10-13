from enum import Enum


class GlobalTop(Enum):
    GLOBAL_TOP = ["рейтинг мира", "рей мира", "топ мира"]


class ChatTop(Enum):
    CHAT_TOP = ["рейтинг чата", "рей чата", "топ чата"]
    CHAT_TOP_DONATE = [f"{i} листвы" for i in CHAT_TOP]
