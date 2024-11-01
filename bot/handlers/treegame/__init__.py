from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Router

from . import users, admin

routers: list[Router] = [*users.routers, *admin.routers]

_all__ = ["routers"]
