from datetime import datetime, timedelta

from bot.config import WALK_WITH_VIP, WALK_WITHOUT_VIP
from bot.database.models import User
from bot.utils.misc import check_datetime


def formatted_heght_tree(height_tree: int) -> str:
    if height_tree < 100:
        return f"{height_tree:_} см".replace("_", " ")
    if height_tree < 1000:
        height_tree = round(height_tree / 100, 1)
        return f"{height_tree:_} м".replace("_", " ")

    height_tree = round(height_tree / 1000, 1)
    return f"{height_tree:_} км".replace("_", " ")


def formatted_next_walk(user: User):
    if check_walk(user):
        return "пора гулять"

    now = datetime.now()
    last_walk = user.last_walk

    next_walk = last_walk + timedelta(hours=walk_time(user))

    return f'до след прогулки {str(next_walk - now).split(".")[0]}'


def formatted_top_number(number: int) -> str:
    medals = {1: "🏅", 2: "🥈", 3: "🥉"}
    return medals.get(number, f" {number}.")


def walk_time(user: User):
    if check_datetime(user.vip_to):
        return WALK_WITH_VIP
    return WALK_WITHOUT_VIP


def check_walk(user: User) -> bool:
    now = datetime.now()
    last_walk = user.last_walk

    if not last_walk:
        return True

    next_walk = last_walk + timedelta(hours=walk_time(user))

    if next_walk - now < timedelta(seconds=1):
        return True
    return False
