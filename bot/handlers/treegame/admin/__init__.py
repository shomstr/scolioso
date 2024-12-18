from __future__ import annotations
from typing import TYPE_CHECKING

from bot.filters import IsAdmin

if TYPE_CHECKING:
    from aiogram import Router

from . import give_items
from . import bot_administrations

routers: list[Router] = [give_items.router, bot_administrations.router]

for router in routers:
    router.message.filter(IsAdmin())
    router.callback_query.filter(IsAdmin())

_all__ = ["routers"]
