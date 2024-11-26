from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Router

from . import start_help, main_menu, top, converter, start_inline, main_menu_inline

routers: list[Router] = [
    start_help.router,
    main_menu.router,
    top.router,
    converter.router,
    start_inline.router,
    main_menu_inline.router,
]

_all__ = ["routers"]
