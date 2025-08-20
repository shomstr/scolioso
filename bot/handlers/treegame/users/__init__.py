from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Router

from . import start, help, gpt
routers: list[Router] = [
    help.help_router,
    start.start_router,
    gpt.gpt_router
]

_all__ = ["routers"]
