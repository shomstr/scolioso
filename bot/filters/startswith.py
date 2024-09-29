from typing import Iterable

from aiogram.filters import BaseFilter
from aiogram.types import Message


class StartsWith(BaseFilter):
    def __init__(self, values: Iterable):
        self.values = values

    async def __call__(self, message: Message) -> bool:
        return any(message.text.lower().startswith(str(value)) for value in self.values)
