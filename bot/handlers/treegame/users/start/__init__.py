from aiogram import Router

from . import start, start_inline

start_router = Router()

start_router.include_routers(start.router, start_inline.router)
