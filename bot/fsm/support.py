from aiogram.fsm.state import State, StatesGroup


class SupportState(StatesGroup):
    question = State()
    screenshot = State()

class OprosState(StatesGroup):
    sex = State()
    age = State()
    ves = State()
    rost = State()
    zabol = State()
    photo = State()


class DefaultPhoto(StatesGroup):
    photo = State()