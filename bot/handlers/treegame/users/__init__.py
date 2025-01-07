from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Router

from . import start, tops, help, mains, gpt, notes, restrics

routers: list[Router] = [
    help.help_router,
    start.start_router,
    tops.top_router,
    mains.main_router,
    gpt.gpt_router,
    notes.notes_router,
    restrics.restrict_router
]

_all__ = ["routers"]
