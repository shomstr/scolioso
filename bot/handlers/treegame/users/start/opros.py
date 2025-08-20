import logging
from bot.utils.model import ScoliosisAnalyzer
from bot.database import Repositories
from aiogram import Router, types, F, Bot
from aiogram.types import Message
from redis.asyncio import Redis
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.fsm.support import OprosState, DefaultPhoto
from bot.settings import settings
from bot.keyboards.default import main2_menu
from aiogram.types import Message, ReplyKeyboardRemove
from bot.handlers.treegame.users.gpt.gpt import gpt_thinks
from bot.keyboards.inline import help_skip_keyboard
 
router = Router(name=__name__)
logger = logging.getLogger()


@router.callback_query(F.data == "start_opros")
async def support(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        "Введите ваш пол\n<blockquote>Пример: Мужской/Женский</blockquote>", reply_markup=main2_menu()
    )
    await state.set_state(OprosState.sex)


@router.message(OprosState.sex, F.text)
async def process_question(msg: Message, state: FSMContext, repo: Repositories):
    sex = msg.text
    await repo.users.add_sex(user_id=msg.from_user.id, sex=sex)
    await state.update_data(sex=msg.text)
    await state.set_state(OprosState.age)
    await msg.answer("Введите ваш возраст\n<blockquote>Пример: 36</blockquote>", reply_markup=ReplyKeyboardRemove())

@router.message(OprosState.age, F.text)
async def process_screenshot(msg: Message, state: FSMContext, repo: Repositories):
    try:
        age = int(msg.text)
        await repo.users.add_age(user_id=msg.from_user.id, age=age)
        await state.update_data(age=age)
        await state.set_state(OprosState.ves)
        await msg.answer("Введите ваш вес\n<blockquote>Пример: 55 (без кг)</blockquote>")
    except ValueError:
        await msg.answer("Пожалуйста, введите число для возраста")

@router.message(OprosState.ves, F.text)
async def process_screenshot(msg: Message, state: FSMContext, repo: Repositories):
    try:
        ves = float(msg.text.replace(',', '.'))  # Handle comma decimals
        await repo.users.add_ves(user_id=msg.from_user.id, ves=ves)
        await state.update_data(ves=ves)
        await state.set_state(OprosState.rost)
        await msg.answer("Введите ваш рост\n<blockquote>Пример: 195 (без см)</blockquote>")
    except ValueError:
        await msg.answer("Пожалуйста, введите число для веса")



@router.message(OprosState.rost, F.text)
async def process_screenshot(msg: Message, state: FSMContext, repo: Repositories):
    age = msg.text
    await repo.users.add_rost(user_id=msg.from_user.id, rost=age)
    await state.update_data(age=msg.text)
    await state.set_state(OprosState.zabol)
    await msg.answer("Введите ваши хронические заболевания связанные со спиной\n<blockquote>Пример: Гиперкифоз\n<i>Только связанное со спиной</i></blockquote>")

@router.message(OprosState.zabol, F.text)
async def process_screenshot(msg: Message, state: FSMContext,repo: Repositories):
    age = msg.text
    await repo.users.add_zab(user_id=msg.from_user.id, zab=age)
    await state.update_data(age=msg.text)
    await state.set_state(OprosState.photo)
    await msg.answer("Пришлите фото\n<blockquote>Пример: Четкий снимок спины</blockquote>")


@router.message(OprosState.photo, F.photo)
async def process_screenshot(msg: Message, state: FSMContext, bot: Bot):
    try:
        # Берем фото наибольшего размера
        photo = msg.photo[-1]

        analyzer = ScoliosisAnalyzer()
        
        # Скачиваем фото
        file = await bot.get_file(photo.file_id)
        file_bytes = await bot.download_file(file.file_path)
        
        # Рассчитываем угол Кобба
        results = analyzer.analyze_scoliosis(file_bytes.getvalue())
        
        # Формируем ответ
       
        await msg.answer(results)
        await state.clear()
        
    except Exception as e:
        await msg.answer("Ошибка обработки фото. Попробуйте другое изображение.")


@router.message(Command('photo'))
async def process_screenshot(msg: Message, state: FSMContext,repo: Repositories):
    age = msg.text
    await repo.users.add_zab(user_id=msg.from_user.id, zab=age)
    await state.update_data(age=msg.text)
    await state.set_state(DefaultPhoto.photo)
    await msg.answer("Пришлите фото\n<blockquote>Пример: Четкий снимок спины</blockquote>")

@router.message(DefaultPhoto.photo, F.photo)
async def process_screenshot(msg: Message, state: FSMContext, bot: Bot, repo: Repositories):
    try:
        analyzer = ScoliosisAnalyzer()
        # Берем фото наибольшего размера
        photo = msg.photo[-1]
        
        # Скачиваем фото
        file = await bot.get_file(photo.file_id)
        file_bytes = await bot.download_file(file.file_path)
        
        # Универсальный способ получения байтов
        if hasattr(file_bytes, 'read'):
            # Если это файловый объект (BufferedReader)
            image_data = file_bytes.read()
            file_bytes.close()  # Важно закрыть файл
        elif hasattr(file_bytes, 'getvalue'):
            # Если это BytesIO или подобный объект
            image_data = file_bytes.getvalue()
        elif isinstance(file_bytes, bytes):
            # Если уже байты
            image_data = file_bytes
        else:
            # Пробуем преобразовать в байты
            image_data = bytes(file_bytes)
        
        # Рассчитываем угол Кобба
        results = analyzer.analyze_scoliosis(image_data)

        # Используем get_by_user_id вместо get_info_by_user_id
        user = await repo.users.get_by_user_id(user_id=msg.from_user.id)
        
        if not user:
            await msg.answer("Информация не найдена. Пожалуйста, заполните информацию о себе. /start")
            return
            
        answ = await gpt_thinks(
            age=int(user.age), 
            sex=user.sex, 
            ves=user.ves, 
            rost=user.rost, 
            zabol=user.zabol, 
            angle=results
        )
       
        await msg.answer(answ)
        await state.clear()
        
    except Exception as e:
        await msg.answer(f"Ошибка обработки фото. Попробуйте другое изображение. {e}")