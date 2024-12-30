
from typing import Sequence, Optional
from datetime import datetime
from sqlalchemy import select, desc, func, delete, update
from sqlalchemy.orm import selectinload, InstrumentedAttribute
from dataclasses import dataclass
from .base import BaseRepo
from bot.database.models import Notes

class NotesRepo(BaseRepo):
    model = Notes

    async def add_note(self, chat_id: int, note_id: int, title: str, note_text: str) -> Notes:

        new_note = self.model(
            chat_id=chat_id,
            note_id=note_id,
            title=title,
            note_text=note_text,
        )
        self.session.add(new_note)
        await self.session.commit()
        return new_note

    async def sel_all_note(self, chat_id: int) -> Sequence[Notes]:
        query = select(self.model).where(self.model.chat_id == chat_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def ex_note(self, chat_id: int, title: str) -> Optional[Notes]:
        query = select(self.model).where(
            self.model.chat_id == chat_id,
            self.model.title == title
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def last_note(self, chat_id: int) -> Optional[int]:
        query = select(func.max(self.model.note_id)).where(self.model.chat_id == chat_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def view_one_note_by_id(self, chat_id: int, note_id: int) -> Optional[Notes]:
        query = select(self.model).where(
            self.model.chat_id == chat_id,
            self.model.note_id == note_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def view_one_note_by_title(self, chat_id: int, title: str) -> Optional[Notes]:
        query = select(self.model).where(
            self.model.chat_id == chat_id,
            self.model.title == title
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def sel_note_for_del(self, chat_id: int, note_id: int) -> Optional[Notes]:
        query = select(self.model).where(
            self.model.chat_id == chat_id,
            self.model.note_id == note_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def del_note_id(self, chat_id: int, note_id: int) -> None:
        await self.session.execute(delete(self.model).where(
            self.model.chat_id == chat_id,
            self.model.note_id == note_id
        ))
        await self.session.commit()

    async def upd_note_list(self, chat_id: int, note_id: int) -> None:
        query = (
            update(self.model).where(
                self.model.chat_id == chat_id,
                self.model.note_id > note_id
            ).values(note_id=self.model.note_id - 1)
        )
        await self.session.execute(query)
        await self.session.commit()

    async def sel_note_title_for_del(self, chat_id: int, note_id_or_title: str) -> Optional[Notes]:
        query = select(self.model).where(
            self.model.chat_id == chat_id,
            self.model.title == note_id_or_title
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def del_note_title(self, chat_id: int, note_id_or_title: str) -> None:
        await self.session.execute(delete(self.model).where(
            self.model.chat_id == chat_id,
            self.model.title == note_id_or_title
        ))
        await self.session.commit()

    async def upd_note_list_for_title(self, chat_id: int, note_id_or_title: str) -> None:
        query = (
            update(self.model).where(
                self.model.chat_id == chat_id,
                self.model.title == note_id_or_title
            ).values(note_id=self.model.note_id - 1)
        )
        await self.session.execute(query)
        await self.session.commit()