from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
)
from aiogram import Bot



async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command = 'start',
            description = 'Запустить бота'
        ),
        BotCommand(
            command = 'help',
            description = 'Помощь'
        ),
        BotCommand(
            command='photo',
            description='Запросить рассчет'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeAllPrivateChats())

async def del_commands(bot: Bot):
    await bot.delete_my_commands(BotCommandScopeAllGroupChats())
    await bot.delete_my_commands(BotCommandScopeAllPrivateChats())
