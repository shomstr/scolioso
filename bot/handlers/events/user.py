import logging

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated

from bot.database.models import User

router = Router()
logger = logging.getLogger()

IS_PRIVATE = F.chat.type == ChatType.PRIVATE


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED), IS_PRIVATE
)
async def user_blocked_bot(event: ChatMemberUpdated, user: User) -> None:
    from_user = event.from_user

    logger.info(f"{from_user.full_name}({from_user.id}) заблокировал бота")


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER), IS_PRIVATE
)
async def user_unblocked_bot(event: ChatMemberUpdated, user: User) -> None:
    from_user = event.from_user

    await event.answer("Привет, спасибо что разблокировал меня")

    logger.info(f"{from_user.full_name}({from_user.id}) разблокировал бота")
