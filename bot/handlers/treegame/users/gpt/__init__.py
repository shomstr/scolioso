from aiogram import Router

from . import gpt

gpt_router = Router()

gpt_router.include_router(gpt.router)
