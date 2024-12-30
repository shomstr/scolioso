import re

from aiogram import Bot, F, Router
from aiogram.types import Message

from bot.database import Repositories
from bot.messages import ADD_NOTE, DEL_NOTE, NOTE_IS_EXIST, VIEW_NOTE_NOT_FOUND
from bot.enums import menus

router = Router()

@router.message(F.text.regexp(menus.re_add_note, mode='fullmatch'))
async def add_note(message: Message, repo: Repositories):
    chat_id = message.chat.id

    title = message.text.splitlines()[0][7:]
    note_text = message.html_text.splitlines()[1:]

    if title.isdigit():
        return await message.answer('🚫 Текст замети не может содержать числа\n<i>Будьте креативнее...</i>')
    existing_note = await repo.notes.ex_note(chat_id, title)
    
    if existing_note:
        await message.answer(NOTE_IS_EXIST)
    else:   
        last_note_value = await repo.notes.last_note(chat_id) 
        last = last_note_value if last_note_value is not None else 0
        note_id = int(last) + 1
              
        await repo.notes.add_note(chat_id, note_id, title, '\n'.join(note_text))
        await message.answer(ADD_NOTE.format(title=title))

@router.message(F.text.regexp(menus.re_del_note, mode='fullmatch'))
async def delete_note(message: Message, repo: Repositories):
    chat_id = message.chat.id

    _, note_id_or_title = message.text.split(maxsplit=1)

    if note_id_or_title.isdigit():
        note_id = int(note_id_or_title)
        note = await repo.notes.view_one_note_by_id(chat_id, note_id)
        
        if note:
            await repo.notes.del_note_id(chat_id, note_id)
            await repo.notes.upd_note_list(chat_id, note.note_id)
            await message.reply(DEL_NOTE.format(note_id=note_id))  
        else:
            await message.answer(VIEW_NOTE_NOT_FOUND) 
    else:
        note_title = note_id_or_title.strip()  
        note = await repo.notes.sel_note_title_for_del(chat_id, note_title)

        if note:
            await repo.notes.del_note_title(chat_id, note_title)
            await repo.notes.upd_note_list(chat_id, note.note_id)
            await message.reply(DEL_NOTE.format(note_title=note_title)) 
        else:
            await message.answer(VIEW_NOTE_NOT_FOUND)  