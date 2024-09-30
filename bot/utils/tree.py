from datetime import datetime, timedelta


def formatted_heght_tree(height_tree: int) -> str:
    if height_tree < 100:
        return f"{height_tree} см"
    if height_tree < 1000:
        return f"{round(height_tree / 100, 1)} м"
    return f"{round(height_tree / 1000, 1)} км"


def formatted_next_walk(last_walk: datetime):
    now = datetime.now()
    if not last_walk:
        return "Можно гулять"

    next_walk = last_walk + timedelta(hours=12)

    if next_walk - now < timedelta(seconds=1):
        return "Можно гулять"

    return f'до след прогулки {str(next_walk - now).split(".")[0]}'


def formatted_top_number(number: int) -> str:
    medals = {1: "🏅", 2: "🥈", 3: "🥉"}
    return medals.get(number, f" {number}.")
