"""
Модуль машины состояний получения анкеты пользователя.
"""

import logging
import sqlite3

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from data.sqlite_men_questionnaire import MensQuestionnaires
from keyboards.inline import channel_markup
from keyboards.replay import replay_keyboard, rmk
from utils.auxiliary_module import administrator_text
from utils.states import StatesQuestionnaire

men_questionnaires_router = Router()
db = MensQuestionnaires()


@men_questionnaires_router.message(F.text == '🙋‍♂️Заполнить мужскую анкету')
async def add_photo(message: types.Message, state: FSMContext) -> None:
    await state.set_state(StatesQuestionnaire.PHOTO)
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Для начала загрузите свою фотографию!"
    )


@men_questionnaires_router.message(StatesQuestionnaire.PHOTO, F.photo)
async def add_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(StatesQuestionnaire.NAME)
    await message.answer("Введите ваше имя:")


@men_questionnaires_router.message(StatesQuestionnaire.PHOTO, ~F.photo)
async def incorrect_photo(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Нужно загрузить фотографию!"
    )


@men_questionnaires_router.message(StatesQuestionnaire.NAME)
async def add_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text, sex='Парень')
    await state.set_state(StatesQuestionnaire.AGE)
    await message.answer("Введите ваш возраст: ")


@men_questionnaires_router.message(StatesQuestionnaire.AGE)
async def add_about(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit() and int(message.text) >= 18:
        await state.update_data(age=int(message.text))
        await state.set_state(StatesQuestionnaire.ABOUT_ME)
        await message.answer("Раскажите немного о себе: ")
    elif message.text.isdigit() and int(message.text) < 18:
        await message.answer("Вам должно быть 18 лет!")
    else:
        await message.answer("Введите возраст числом!")


@men_questionnaires_router.message(StatesQuestionnaire.ABOUT_ME)
async def add_find_me(message: types.Message, state: FSMContext) -> None:
    await state.update_data(about_me=message.text)
    await state.set_state(StatesQuestionnaire.FIND)
    menu = await replay_keyboard(['Парень', 'Девушка'])
    await message.answer("Кого вы хотите найти?", reply_markup=menu)


@men_questionnaires_router.message(StatesQuestionnaire.FIND, F.text.casefold().in_(['парень', 'девушка']))
async def check_status(message: types.Message, state: FSMContext) -> None:
    await state.update_data(gender=message.text)
    await state.set_state(StatesQuestionnaire.STATUS)
    menu = await replay_keyboard(['Хочу', 'Не хочу'])
    await message.answer("Вы хотите чтобы ваша анкета показывалась другим пользователям?", reply_markup=menu)


@men_questionnaires_router.message(StatesQuestionnaire.STATUS, F.text.casefold().in_(['хочу', 'не хочу']))
async def check_status(message: types.Message, state: FSMContext) -> None:
    await state.update_data(status=message.text)
    data = await state.get_data()
    await state.clear()
    photo = data.get('photo')
    text = administrator_text(data)
    await message.answer_photo(photo, text,)
    await message.answer('*****', reply_markup=rmk)
    await message.answer(f"{data.get('name')}\n"
                         f"Спасибо! Ваша анкета отправлена на модерацию. Мы сообщим о успешном прохождении!",
                         reply_markup=channel_markup)
    try:
        db.add_profile(
            user_id=message.from_user.id,
            photo=photo,
            user_name=data.get('name'),
            gender=data.get('sex'),
            age=data.get('age'),
            about_me=data.get('about_me'),
            status=data.get('status'),
            finding=data.get('gender')
        )
        logging.info("Added profile man")
    except sqlite3.IntegrityError:
        logging.info("Пользователь уже зарегистрирован")


@men_questionnaires_router.message(StatesQuestionnaire.FIND)
async def incorrect_gender(message: types.Message, state: FSMContext) -> None:
    menu = await replay_keyboard(['Парень', 'Девушка'])
    await message.answer("Выберите кого вы хотите найти!", reply_markup=menu)
