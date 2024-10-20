import re

from aiogram.filters import Filter
from aiogram.types import Message

from bot.utils.aiogram import get_user_from_message


class FullmatchWithArgs(Filter):
    def __init__(self, *commands, user: bool = True, count: bool = True):
        self.commands = commands
        self.user = user
        self.count = count

        self.pattern = r"^{command}"
        self.pattern_with_reply = r"^{command}"

        if user:
            self.pattern += r"\s(@\w+)?"
        if count:
            self.pattern += r"\s(?P<count>\d+)"
            self.pattern_with_reply += r"\s(?P<count>\d+)"

        self.pattern += r"$"  # Закрываем шаблон
        self.pattern_with_reply += r"$"

    async def __call__(self, message: Message) -> bool | dict:
        if not message.text:
            return False

        for command in self.commands:
            if message.reply_to_message:
                pattern = self.pattern_with_reply.format(command=command)
            else:
                pattern = self.pattern.format(command=command)

            if e := re.fullmatch(pattern, message.text.lower()):
                t = e.groupdict()
                return {
                    "command": command,
                    "us": get_user_from_message(message, command) if self.user else None,
                    "count": int(t.get("count")) if self.count else None,
                }

        return False


class Fullmatch(Filter):
    def __init__(self, *commands):
        self.commands = commands

    async def __call__(self, message: Message) -> bool | dict:
        if not message.text:
            return False

        for command in self.commands:
            if message.text.lower() == command.lower():
                return {"command": command}

        return False
