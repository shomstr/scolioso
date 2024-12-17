import logging

from aiogram import Router, types, F, Bot
from aiogram.types import Message
from redis.asyncio import Redis
from aiogram.fsm.context import FSMContext
from bot.fsm.support import SupportState
from bot.settings import settings
from bot.keyboards.inline import help_skip_keyboard

router = Router(name=__name__)
logger = logging.getLogger()


@router.callback_query(F.data == "help_support")
async def support(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        "Введите ваше обращение и прикрепите скрин ниже при необходимости"
    )
    await state.set_state(SupportState.question)


@router.message(SupportState.question, F.text)
async def process_question(msg: Message, state: FSMContext):
    await msg.answer(
        f"Ваш вопрос: {msg.text}, хотите прикрепить скрин? если нет нажми проупустить, если проблема решена жми отмена",
        reply_markup=help_skip_keyboard(),
    )
    await state.update_data(question=msg.text)
    await state.set_state(SupportState.screenshot)


@router.message(SupportState.screenshot, F.photo)
async def process_screenshot(msg: Message, state: FSMContext, bot: Bot, redis: Redis):

    photo_data = msg.photo[-1].file_id
    data = await state.get_data()

    question = data.get("question")
    await state.update_data(screenshot=photo_data)

    await bot.send_photo(
        chat_id=settings.support.id,
        photo=f"{photo_data}",
        caption=f"новое обращение от игрока:\n{question}"
    )
    await redis.hset(name='support', key=msg.from_user.id, value=msg.message_id)

    await msg.answer("Обращение отправлено!\nожидайте ответа от поддержки.")
