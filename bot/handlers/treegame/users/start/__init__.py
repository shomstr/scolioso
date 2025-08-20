from aiogram import Router

from . import start, start_inline, opros

start_router = Router()

start_router.include_routers(start.router, start_inline.router, opros.router)
