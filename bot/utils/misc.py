import contextlib
import html
import platform
import subprocess
import sys
import time
from datetime import timedelta, datetime
from typing import Any

import aiogram
import psutil

from bot.database import get_repo

time_st = time.perf_counter()


def bytes_to_megabytes(b: float) -> float:
    return round(b / 1024 / 1024, 1)


def uptime() -> int:
    """
    Returns bot uptime in seconds
    :return: Uptime in seconds
    """
    return round(time.perf_counter() - time_st)


def formatted_uptime() -> str:
    """
    Returnes formmated uptime
    :return: Formatted uptime
    """
    return str(timedelta(seconds=uptime()))


async def bot_info_dict() -> dict[str, Any]:
    """Возращает данные про бота и серв"""
    inf = {
        "cpu": "n/a",
        "cpu_load": "n/a",
        "ram": "n/a",
        "ram_load_mb": "n/a",
        "ram_load": "n/a",
        "arch_emoji": "n/a",
        "arch": "n/a",
        "os": "n/a",
        "python": "n/a",
        "aiogram": aiogram.__version__,
        "process_ram": "n/a",
        "process_ram_percent" "process_cpu_percent": "n/a",
        "bot_working": formatted_uptime(),
        "users_in_db": 0,
    }

    with contextlib.suppress(Exception):
        inf["cpu"] = psutil.cpu_count(logical=True)

    with contextlib.suppress(Exception):
        inf["cpu_load"] = psutil.cpu_percent()

    with contextlib.suppress(Exception):
        inf["ram"] = bytes_to_megabytes(
            psutil.virtual_memory().total - psutil.virtual_memory().available
        )

    with contextlib.suppress(Exception):
        inf["ram_load_mb"] = bytes_to_megabytes(psutil.virtual_memory().total)

    with contextlib.suppress(Exception):
        inf["ram_load"] = psutil.virtual_memory().percent

    with contextlib.suppress(Exception):
        inf["arch"] = html.escape(platform.architecture()[0])

    inf["arch_emoji"] = (
        "<emoji document_id=5172881503478088537>💻</emoji>"
        if "64" in inf.get("arch", "")
        else "<emoji document_id=5174703196676817427>💻</emoji>"
    )

    with contextlib.suppress(Exception):
        with subprocess.Popen(
            "cat /etc/*release", stdout=subprocess.PIPE, shell=True
        ) as proc:
            if proc.stdout:
                system = proc.stdout.read().decode("utf-8")
                b = system.find('DISTRIB_DESCRIPTION="') + 21
                system = system[b : system.find('"', b)]
                inf["os"] = html.escape(system)

    with contextlib.suppress(Exception):
        inf["python"] = (
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )

    # process
    process = psutil.Process()

    with contextlib.suppress(Exception):
        inf["process_ram"] = bytes_to_megabytes(process.memory_info().rss)

    with contextlib.suppress(Exception):
        inf["process_ram_percent"] = round(process.memory_percent(), 1)

    with contextlib.suppress(Exception):
        inf["process_cpu_percent"] = round(process.cpu_percent(), 1)

    async with get_repo() as repo:
        inf["users_in_db"] = await repo.users.get_all(count=True)

    return inf


def check_datetime(time: datetime) -> bool:
    """
    :param time_in_timestamp:
    :return: True если дата в time больше чем сегодняшняя
    """

    if not time:
        return True

    now = datetime.now()

    if time > now:
        return True
    return False


def datetime_to_str(date: datetime) -> str:
    if not date:
        return "Навсегда"

    now = datetime.now()

    if (date - now) >= timedelta(days=1):
        d = date.strftime("%d.%m.%Y")
        return f"{d} ({(date - now).days} дней)"

    d = date - now
    return str(d).split(".")[0]
