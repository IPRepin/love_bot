"""
Модуль машины состояний получения анкеты пользователя.
"""

import asyncio
import logging
import sqlite3

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from keyboards.replay import find_gender_keyboard, status_keyboard
from utils.states import MenQuestionnaire

men_questionnaires_router = Router()


@men_questionnaires_router.message(F.text == '🙋‍♂️Заполнить мужскую анкету')
async def add_photo(message: types.Message, state: FSMContext) -> None:
    await state.set_state(MenQuestionnaire.PHOTO)
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Для начала загрузите свою фотографию!"
    )


@men_questionnaires_router.message(MenQuestionnaire.PHOTO, F.photo)
async def add_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(MenQuestionnaire.NAME)
    await message.answer("Введите ваше имя:")


@men_questionnaires_router.message(MenQuestionnaire.PHOTO, ~F.photo)
async def incorrect_photo(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Нужно загрузить фотографию!"
    )


@men_questionnaires_router.message(MenQuestionnaire.NAME)
async def add_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text, gender='Парень')
    await state.set_state(MenQuestionnaire.AGE)
    await message.answer("Введите ваш возраст: ")


@men_questionnaires_router.message(MenQuestionnaire.AGE)
async def add_about(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit() and int(message.text) >= 18:
        await state.update_data(age=int(message.text))
        await state.set_state(MenQuestionnaire.ABOUT_ME)
        await message.answer("Раскажите немного о себе: ")
    elif message.text.isdigit() and int(message.text) < 18:
        await message.answer("Вам должно быть 18 лет!")
    else:
        await message.answer("Введите возраст числом!")


@men_questionnaires_router.message(MenQuestionnaire.ABOUT_ME)
async def add_find_me(message: types.Message, state: FSMContext) -> None:
    await state.update_data(about_me=message.text)
    await state.set_state(MenQuestionnaire.FIND)
    menu = await find_gender_keyboard(['Парень', 'Девушка'])
    await message.answer("Кого вы хотите найти?", reply_markup=menu)


@men_questionnaires_router.message(MenQuestionnaire.FIND, F.text.casefold().in_(['парень', 'девушка']))
async def check_status(message: types.Message, state: FSMContext) -> None:
    await state.update_data(gender=message.text)
    await state.set_state(MenQuestionnaire.STATUS)
    menu = await status_keyboard(['Хочу', 'Не хочу'])
    await message.answer("Вы хотите чтобы ваша анкета показывалась другим пользователям?", reply_markup=menu)


@men_questionnaires_router.message(MenQuestionnaire.STATUS, F.text.casefold().in_(['хочу', 'не хочу']))
async def check_status(message: types.Message, state: FSMContext) -> None:
    await state.update_data(status=message.text)
    data = await state.get_data()
    await state.clear()
    photo = data.get('photo')
    form_msg = []
    [
        form_msg.append(f'{key}: {value}')
        for key, value in data.items()
    ]
    await message.answer_photo(
        photo,
        "\n".join(form_msg[1:]),
    )


@men_questionnaires_router.message(MenQuestionnaire.FIND)
async def incorrect_gender(message: types.Message, state: FSMContext) -> None:
    menu = await find_gender_keyboard(['Парень', 'Девушка'])
    await message.answer("Выберите кого вы хотите найти!", reply_markup=menu)
