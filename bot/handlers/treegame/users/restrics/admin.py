from aiogram import Router, Bot, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums.chat_type import ChatType

from bot.utils import bot_commands 

router = Router()

@router.message(F.text.lower() == 'убкл')
async def echo(message: Message, bot: Bot):

    if ChatType.PRIVATE:
        return

    result: Union[ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMemberRestricted] = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)

    if result.status == 'creator' or result.status == 'administrator':
        await message.answer(f"успешно убрана клавиатура", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Вы не являетесь создателем или администратором данного чата")

@router.message(F.text.lower() == 'убком')
async def echo(message: Message, bot: Bot):

    if ChatType.PRIVATE:
        return
        
    result: Union[ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMemberRestricted] = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)

    if result.status == 'creator' or result.status == 'administrator':
        await bot_commands.del_commands(bot)
        await message.answer(f"успешно убрана клавиатура")
    else:
        await message.answer("Вы не являетесь создателем или администратором данного чата")