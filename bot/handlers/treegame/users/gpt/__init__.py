from aiogram import Router

from . import gpt_handler

gpt_router = Router()

gpt_router.include_router(gpt_handler.router)
