import logging
from typing import Any

from aiogram import Router, F
from aiogram.types import Message
from bot.database.repos.users import UsersRepo
from bot.database import Repositories
from bot.enums.admin_panel import MessageCommands
from bot.filters import Fullmatch
from bot.utils.aiogram import get_user_by_username, send_message

router = Router()
logger = logging.getLogger(__name__)


@router.message(Fullmatch(*MessageCommands.ADMIN_PANEL.value))
async def admin_panel(message: Message, repo: Repositories):
    all_users = await repo.users.get_all_users()
    all_chats = await repo.chats.get_all_chats()

    user_count = len(all_users)
    chats_count = len(all_chats)

    await message.answer(f'всего <b>{user_count}</b> пользователей и <b>{chats_count}</b> чата в боте')