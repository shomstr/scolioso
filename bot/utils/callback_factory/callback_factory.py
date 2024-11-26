from aiogram.filters.callback_data import CallbackData


class MyCallback(CallbackData, prefix="my"):
    test: int
    test1: str


class prev_data(CallbackData, prefix="help_prev"):
    skill: str
    num: int


class next_data(CallbackData, prefix="next_help"):
    skill: str
    num: int
