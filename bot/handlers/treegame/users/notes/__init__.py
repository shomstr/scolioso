from aiogram import Router

from . import notes_oprations, view_notes

notes_router = Router()

notes_router.include_routers(notes_oprations.router, view_notes.router)