from aiogram import Router

from . import help, help_inline, support

help_router = Router()

help_router.include_routers(help.router, help_inline.router, support.router)
