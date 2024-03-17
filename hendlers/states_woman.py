"""
Модуль машины состояний получения анкеты пользователя.
"""

import sqlite3

from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext

from data.sqlite_woman_questionnaire import WomanQuestionnaires
from filters.photo_filter import has_face
from keyboards.replay import gen_replay_keyboard, edit_profile_markup
from utils.admins import get_random_admin
from utils.auxiliary_module import administrator_text
from utils.states import StatesWomanQuestionnaire

from utils.logs_hendler_telegram import setup_logger

logger = setup_logger()
woman_questionnaires_router = Router()
db = WomanQuestionnaires()


@woman_questionnaires_router.message(F.text == '🙋‍♀️Заполнить женскую анкету')
async def add_photo(message: types.Message, state: FSMContext) -> None:
    setup_logger().info('Заполнение анкеты девушка')
    await state.set_state(StatesWomanQuestionnaire.PHOTO)
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Для начала загрузите свою фотографию!"
    )


@woman_questionnaires_router.message(StatesWomanQuestionnaire.PHOTO, F.photo)
async def add_name(message: types.Message, state: FSMContext) -> None:
    # file_id = message.photo[-1].file_id
    # file = await bot.get_file(file_id)
    # file_path = file.file_path
    # file_bytes = await bot.download_file(file_path)
    # if has_face(file_bytes):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(StatesWomanQuestionnaire.NAME)
    await message.answer("Введите ваше имя:")
    # else:
    #     await message.answer("Нет лица на фотографии!")


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
        await state.update_data(age=int(message.text), user_url=message.from_user.url)
        await state.set_state(StatesWomanQuestionnaire.ABOUT_ME)
        await message.answer("Раскажите немного о себе: ")
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


@woman_questionnaires_router.message(StatesWomanQuestionnaire.FIND, F.text.casefold().in_(['парень', 'девушка']))
async def check_status(message: types.Message, state: FSMContext) -> None:
    await state.update_data(find_gender=message.text)
    await state.set_state(StatesWomanQuestionnaire.STATUS)
    menu = await gen_replay_keyboard(['Хочу', 'Не хочу'])
    await message.answer("Вы хотите чтобы ваш контакт телеграм был виден другим пользователям?", reply_markup=menu)


@woman_questionnaires_router.message(StatesWomanQuestionnaire.STATUS,
                                     F.text.casefold().in_(['хочу', 'не хочу']))
async def check_status(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(status=message.text)
    data = await state.get_data()
    await state.clear()
    photo = data.get('photo')
    text = administrator_text(data)
    try:
        db.add_profile(
            user_id=message.from_user.id,
            photo=photo,
            user_name=data.get('name'),
            user_url=data.get('user_url'),
            gender=data.get('sex'),
            age=data.get('age'),
            about_me=data.get('about_me'),
            status=data.get('status'),
            finding=data.get('find_gender')
        )
        admin_id = get_random_admin()
        await bot.send_photo(chat_id=309052693, photo=photo, caption=text)
        await message.answer(text=f"{data.get('name')}\n"
                                  f"Спасибо! Ваша анкета отправлена на модерацию. \n"
                                  f"ДОКАЖИТЕ, ЧТО ВЫ НЕ ФЕЙК\n"
                                  f"ОТПРАВЬТЕ ВИДЕОСООБЩЕНИЕ С ФРАЗОЙ 'ДЛЯ КАНАЛА ЗНАКОМСТВ'\n"
                                  f" на <a href='...'>ОТПРАВЛЯТЬ СЮДА</a>.</i>"
                                  f"Мы сообщим об успешном прохождении модерации.",
                             reply_markup=edit_profile_markup,
                             disable_web_page_preview=True, )
        logger.info("Added profile man")
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
