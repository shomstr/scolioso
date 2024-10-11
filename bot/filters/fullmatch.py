import re

from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.utils.aiogram import get_user_from_message


class Fullmatch(BaseFilter):
    def __init__(self, *commands, user: bool = True, count: bool = True):
        self.commands = commands
        self.user = user
        self.count = count

        self.pattern = r"^{command}"
        if user:
            self.pattern += r"\s(?P<user>@\w+)"  # Исправлено
        if count:
            self.pattern += r"\s(?P<count>\d+)"  # Исправлено
        self.pattern += r"$"  # Закрываем шаблон

    async def __call__(self, message: Message) -> bool | dict:
        if not message.text:
            return False

        for command in self.commands:
            if e := re.fullmatch(self.pattern.format(command=command), message.text.lower()):
                t = e.groupdict()
                return {
                    "command": command,
                    "us": get_user_from_message(message, command) if self.user else None,
                    "count": int(t.get("count")) if self.count else None,
                }

        return False
