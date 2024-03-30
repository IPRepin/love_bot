"""Функции обработки кнопок основного меню"""
import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires
from hendlers.states_man import add_photo as men_add_photo
from hendlers.states_woman import add_photo as women_add_photo
from keyboards.inline import buy_subscription_markup, support_button
from keyboards.replay import main_markup, edit_profile_markup

logger = logging.getLogger(__name__)
db_men = MensQuestionnaires()
db_woman = WomanQuestionnaires()
main_users_router = Router()


@main_users_router.callback_query(F.data.in_(['cancel', 'cancel_main']))
async def cancel_btn(query: types.CallbackQuery):
    if query.data == 'cancel':
        await query.message.answer("С возвращением\n"
                                   "\n"
                                   "<i>Продолжая, вы принимаете\n"
                                   "<a href='https://znfkomstobot.tilda.ws/'>"
                                   "Пользовательское соглашение</a></i>",
                                   reply_markup=main_markup
                                   )
        await query.answer()
    elif query.data == 'cancel_main':
        await query.message.answer('Главное меню',
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
    logger.info("Функция delete_questionnaires вызвана")
    logger.info(f"{message.from_user.id}")
    if db_men.profile_exists(user_id=message.from_user.id):
        db_men.delete_profile(user_id=message.from_user.id)
        await message.answer(f"{message.from_user.first_name}\n"
                             "Ваша анкета была удалена.\n"
                             "Хотите заполнить новую?",
                             reply_markup=main_markup)
    elif db_woman.profile_exists(user_id=message.from_user.id):
        db_woman.delete_profile(user_id=message.from_user.id)
        await message.answer(f"{message.from_user.first_name}\n"
                             "Ваша анкета была удалена.\n"
                             "Хотите заполнить новую?",
                             reply_markup=main_markup)
    else:
        logger.error("Функция delete_questionnaires вызвана, но не удалила анкету")


@main_users_router.message(F.text == '✏️Отредактировать анкету')
async def edit_questionnaires(message: types.Message, state: FSMContext) -> None:
    logger.info("Функция edit_questionnaires вызвана")
    logger.info(f"{message.from_user.id}")
    if db_men.profile_exists(user_id=message.from_user.id):
        db_men.delete_profile(user_id=message.from_user.id)
        await men_add_photo(message, state)
    elif db_woman.profile_exists(user_id=message.from_user.id):
        db_woman.delete_profile(user_id=message.from_user.id)
        await women_add_photo(message, state)
    else:

        logger.error("Функция edit_questionnaires вызвана, но не отредактировала анкету")


@main_users_router.message(F.text == '📩Связатся с администратором')
async def write_administrator(message: types.Message) -> None:
    await message.answer(f"{message.from_user.first_name} если у вас "
                         f"возникли вопросы по заполнению анкеты, свяжитесь "
                         f"с нами нажав кнопку ниже ⬇️",
                         reply_markup=support_button)
