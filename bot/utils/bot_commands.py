from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from aiogram import Bot


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🌲 Начать играть"),
        BotCommand(command="help", description="☎️ Помощь и поддержка"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeAllPrivateChats())


async def del_commands(bot: Bot):
    await bot.delete_my_commands(BotCommandScopeAllGroupChats())
    await bot.delete_my_commands(BotCommandScopeAllPrivateChats())
