from aiogram import Router

from . import main_menu, main_menu_inline, converter

main_router = Router()

main_router.include_routers(main_menu.router, main_menu_inline.router, converter.router)
