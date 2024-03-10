"""
Модуль машины состояний получения анкеты пользователя.
"""

import asyncio
import logging
import sqlite3

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from utils.states import MenQuestionnaire

men_questionnaires_router = Router()


@men_questionnaires_router.message(F.text == '🙋‍♂️Заполнить мужскую анкету')
async def add_photo(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Загрузи свою фотографию"
    )
    await state.set_state(MenQuestionnaire.PHOTO)
