from datetime import datetime, timedelta


def formatted_heght_tree(height_tree: int) -> str:
    if height_tree < 100:
        return f"{height_tree} см"
    if height_tree < 1000:
        return f"{round(height_tree / 100, 1)} м"
    return f"{round(height_tree / 1000, 1)} км"


def formatted_next_walk(last_walk: datetime):
    now = datetime.now()
    next_walk = last_walk + timedelta(hours=12)
    return str(next_walk - now).split(".")[0]
