from . import admin 

from aiogram import Router


restrict_router = Router()

restrict_router.include_router(admin.router)