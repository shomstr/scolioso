from aiogram import Router

from . import top

top_router = Router()

top_router.include_router(top.router)
