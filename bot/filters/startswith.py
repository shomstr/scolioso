from typing import Iterable

from aiogram.filters import BaseFilter
from aiogram.types import Message


class StartsWith(BaseFilter):
    def __init__(self, values: Iterable):
        self.values = values

    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False

        for value in self.values:
            if message.text.lower().startswith(str(value)):
                return {"command": str(value)}
        return False
