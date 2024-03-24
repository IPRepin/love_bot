"""Функции обработки кнопок основного меню"""
import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires
from hendlers.states_man import add_photo as men_add_photo
from hendlers.states_woman import add_photo as women_add_photo
from keyboards.inline import buy_subscription_markup
from keyboards.replay import main_markup, edit_profile_markup

logger = logging.getLogger(__name__)
db_men = MensQuestionnaires()
db_woman = WomanQuestionnaires()
main_users_router = Router()


@main_users_router.callback_query(F.data == 'cancel' or F.data == 'back')
async def cancel_btn(query: types.CallbackQuery):
    if query.data == 'cancel':
        await query.message.answer(f"С возвращением\n"                                 
                                   f"\n"
                                   f"<i>Продолжая, вы принимаете\n"
                                   f"<a href='https://znfkomstobot.tilda.ws/'>Пользовательское соглашение</a></i>",
                                   reply_markup=main_markup
                                   )
        await query.answer()
    elif query.data == 'back':
        await query.message.answer(f"С возвращением\n"
                                   f"\n"
                                   f"<i>Продолжая, вы принимаете\n"
                                   f"<a href='https://znfkomstobot.tilda.ws/'>Пользовательское соглашение</a></i>",
                                   reply_markup=edit_profile_markup
                                   )
        await query.answer()


@main_users_router.message(F.text == '💞Оформить подписку')
async def buy_subscription(message: types.Message) -> None:
    await message.answer("Возможно Вы не готовы пока оставлять свою анкету,"
                         " но хотите получить доступ к контактам - "
                         "это можно сделать оформив подписку.\n",
                         reply_markup=buy_subscription_markup)


@main_users_router.message(F.text == "🗑️Удалить анкету")
async def delete_questionnaires(message: types.Message) -> None:
    logger.info(f"Функция delete_questionnaires вызвана")
    logger.info(f"{message.from_user.id}")
    if db_men.profile_exists(user_id=message.from_user.id):
        db_men.delete_profile(user_id=message.from_user.id)
        await message.answer(f"{message.from_user.first_name}\n"
                             f"Ваша анкета была удалена.\n"
                             f"Хотите заполнить новую?",
                             reply_markup=main_markup)
    elif db_woman.profile_exists(user_id=message.from_user.id):
        db_woman.delete_profile(user_id=message.from_user.id)
        await message.answer(f"{message.from_user.first_name}\n"
                             f"Ваша анкета была удалена.\n"
                             f"Хотите заполнить новую?",
                             reply_markup=main_markup)
    else:
        logger.error(f"Функция delete_questionnaires вызвана, но не удалила анкету")


@main_users_router.message(F.text == '✏️Отредактировать анкету')
async def edit_questionnaires(message: types.Message, state: FSMContext) -> None:
    logger.info(f"Функция edit_questionnaires вызвана")
    logger.info(f"{message.from_user.id}")
    if db_men.profile_exists(user_id=message.from_user.id):
        db_men.delete_profile(user_id=message.from_user.id)
        await men_add_photo(message, state)
    elif db_woman.profile_exists(user_id=message.from_user.id):
        db_woman.delete_profile(user_id=message.from_user.id)
        await women_add_photo(message, state)
    else:
        logger.error(f"Функция edit_questionnaires вызвана, но не отредактировала анкету")
