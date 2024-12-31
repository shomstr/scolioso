from aiogram.filters.callback_data import CallbackData


class MyCallback(CallbackData, prefix="my"):
    test: int
    test1: str


class prev_data(CallbackData, prefix="help_prev"):
    skill: str
    num: int


class next_data(CallbackData, prefix="help_next"):
    skill: str
    num: int

class kl_tree_data(CallbackData, prefix="tree"):
    skill: str
    id: int

class kl_walking_data(CallbackData, prefix="watering"):
    skill: str
    id: int

class kl_watering_data(CallbackData, prefix="walking"):
    skill: str
    id: int