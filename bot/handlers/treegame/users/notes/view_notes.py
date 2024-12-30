import re
from aiogram import Bot, Router, F
from aiogram.types import Message
from datetime import datetime
from bot.database import Repositories
from bot.messages import VIEW_NOTE, VIEW_NOTE_NOT_FOUND, VIEW_NOTES, VIEW_NOTES_NOT_FOUND, NOTE_IS_EXIST
from bot.enums import menus

router = Router()

@router.message(F.text.regexp(menus.re_show_all_notes, mode='fullmatch'))
async def view_notes(message: Message, repo: Repositories):
    chat_id = message.chat.id
    notes = await repo.notes.sel_all_note(chat_id)
    
    if notes:
        notes_text = "\n".join([
            f" 🌱 {i + 1}. {note.title} ({note.created_at.strftime('%d.%m.%Y')})" 
            for i, note in enumerate(notes)
        ])
        await message.answer(VIEW_NOTES.format(notes=notes_text), parse_mode='HTML') 
    else:
        await message.answer(VIEW_NOTES_NOT_FOUND)

@router.message(F.text.regexp(menus.re_show_note, mode='fullmatch'))
async def view_one_note(message: Message, repo: Repositories):
    chat_id = message.chat.id
 
    _, identifier = message.text.split(maxsplit=1)

    if identifier.isdigit():
        note_id = int(identifier)
        note = await repo.notes.view_one_note_by_id(chat_id, note_id)
    else:
        title = identifier.strip()
        note = await repo.notes.view_one_note_by_title(chat_id, title)

    if note:
        note_title = note.title
        note_text = note.note_text
        time = note.created_at.strftime("%d.%m.%Y")  
        await message.reply(VIEW_NOTE.format(note_title=note_title, note_text=note_text, time=time))
    else:
        await message.answer(VIEW_NOTE_NOT_FOUND)
