from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Router

from . import start_help, main_menu, top, converter

routers: list[Router] = [start_help.router, main_menu.router, top.router, converter.router]

_all__ = ["routers"]
