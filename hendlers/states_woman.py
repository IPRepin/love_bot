"""
Модуль машины состояний получения анкеты пользователя.
"""
import logging
import sqlite3

from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from data.sqlite_woman_questionnaire import WomanQuestionnaires
from filters.admins_filter import get_random_admin
from filters.photo_filter import has_face
from keyboards.inline import moderation_keyboard, send_video
from keyboards.replay import gen_replay_keyboard, edit_profile_markup
from utils.auxiliary_module import administrator_text
from utils.states import StatesWomanQuestionnaire, UserIdState

logger = logging.getLogger(__name__)
woman_questionnaires_router = Router()
db = WomanQuestionnaires()
load_dotenv()


@woman_questionnaires_router.message(F.text == '🙋‍♀️Заполнить женскую анкету')
async def add_photo(message: types.Message, state: FSMContext) -> None:
    logger.info('Заполнение анкеты девушка')
    await state.set_state(StatesWomanQuestionnaire.PHOTO)
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Для начала загрузите свою фотографию!"
    )


@woman_questionnaires_router.message(StatesWomanQuestionnaire.PHOTO, F.photo)
async def add_name(message: types.Message, state: FSMContext, bot: Bot) -> None:
    file_id = message.photo[-1].file_id
    download_file = await bot.get_file(file_id)
    file_path = download_file.file_path
    file_bytes = await bot.download_file(file_path)
    if has_face(file_bytes):
        await state.update_data(photo=message.photo[-1].file_id)
        await state.set_state(StatesWomanQuestionnaire.NAME)
        await message.answer("Введите ваше имя:")
    else:
        await message.answer("Нет лица на фотографии!")


@woman_questionnaires_router.message(StatesWomanQuestionnaire.PHOTO, ~F.photo)
async def incorrect_photo(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Нужно загрузить фотографию!"
    )


@woman_questionnaires_router.message(StatesWomanQuestionnaire.NAME)
async def add_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text, sex='Женский')
    await state.set_state(StatesWomanQuestionnaire.AGE)
    await message.answer("Введите ваш возраст: ")


@woman_questionnaires_router.message(StatesWomanQuestionnaire.AGE)
async def add_about(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit() and int(message.text) >= 18:
        await state.update_data(age=int(message.text), user_url=f"@{message.from_user.username}")
        await state.set_state(StatesWomanQuestionnaire.ABOUT_ME)
        await message.answer("🎨Увлечения, хобби: ")
    elif message.text.isdigit() and int(message.text) < 18:
        await message.answer("Вам должно быть 18 лет!")
    else:
        await message.answer("Введите возраст целым числом!")


@woman_questionnaires_router.message(StatesWomanQuestionnaire.ABOUT_ME)
async def add_find_me(message: types.Message, state: FSMContext) -> None:
    await state.update_data(about_me=message.text)
    await state.set_state(StatesWomanQuestionnaire.FIND)
    menu = await gen_replay_keyboard(['Парень', 'Девушка'])
    await message.answer("Кого вы хотите найти?", reply_markup=menu)


@woman_questionnaires_router.message(StatesWomanQuestionnaire.FIND,
                                     F.text.casefold().in_(['парень', 'девушка']))
async def check_status(message: types.Message, state: FSMContext) -> None:
    await state.update_data(find_gender=message.text)
    await state.set_state(StatesWomanQuestionnaire.STATUS)
    menu = await gen_replay_keyboard(['Только телеграм'])
    await message.answer("Здесь вы можете оставить свой никнейм в любой из соц сетей\n"
                         "либо нажмите на кнопку ниже если хотите оставить только телеграм.",
                         reply_markup=menu)


@woman_questionnaires_router.message(StatesWomanQuestionnaire.STATUS)
async def final_status(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(social_network=message.text)
    data = await state.get_data()
    await state.clear()
    user_id = message.from_user.id
    photo = data.get('photo')
    text = administrator_text(data)
    try:
        db.add_profile(
            user_id=user_id,
            photo=photo,
            user_name=data.get('name'),
            user_url=data.get('user_url'),
            gender=data.get('sex'),
            age=data.get('age'),
            about_me=data.get('about_me'),
            social_network=data.get('social_network'),
            finding=data.get('find_gender')
        )
        admin_id = get_random_admin()
        await bot.send_photo(chat_id=admin_id,
                             photo=photo,
                             caption="❗❗Пришла новая анкета!❗❗\n"
                                     f"user_id: {message.from_user.id}\n"
                                     f"{text}\n"
                                     f"Нажмите на кнопку '⏩Проверить анкеты'",
                             # reply_markup=moderation_keyboard
                             )
        await message.answer(text=f"{data.get('name')}\n"
                                  f"✅Спасибо! Ваша анкета отправлена на модерацию.\n"
                                  f"ДОКАЖИТЕ, ЧТО ВЫ НЕ ФЕЙК\n"
                                  f'ОТПРАВЬТЕ ВИДЕОСООБЩЕНИЕ С ФРАЗОЙ "ДЛЯ КАНАЛА ЗНАКОМСТВ"\n'
                                  f"НАЖАВ НА КНОПКУ '📽Отправить видео'\n"
                                  f"Мы сообщим об успешном прохождении модерации.",
                             reply_markup=send_video,
                             disable_web_page_preview=True, )
        await message.answer("Меню⬇️", reply_markup=edit_profile_markup)
        logger.info("Added profile woman")
    except sqlite3.IntegrityError as error:
        logger.error(error)
        logger.error("Пользователь уже зарегистрирован")
        await message.answer(f"{data.get('name')}\n"
                             f"Вы уже заполняли анкету.",
                             reply_markup=edit_profile_markup)


@woman_questionnaires_router.message(StatesWomanQuestionnaire.FIND)
async def incorrect_gender(message: types.Message, state: FSMContext) -> None:
    menu = await gen_replay_keyboard(['Парень', 'Девушка'])
    await message.answer("Выберите кого вы хотите найти!", reply_markup=menu)
