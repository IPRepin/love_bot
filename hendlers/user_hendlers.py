"""Функции обработки кнопок основного меню"""
import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires
from hendlers.states_man import add_photo as men_add_photo
from hendlers.states_woman import add_photo as women_add_photo
from keyboards.inline import buy_subscription_markup, go_to_free_chat
from keyboards.replay import main_markup, edit_profile_markup

logger = logging.getLogger(__name__)
db_men = MensQuestionnaires()
db_woman = WomanQuestionnaires()
main_users_router = Router()


@main_users_router.callback_query(F.data == 'cancel')
async def cancel_btn(query: types.CallbackQuery):
    await query.message.answer(f"С возвращением {query.message.from_user.first_name}\n"
                               f"Хочеш запонить еще одну анкету❓\n"
                               f"\n"
                               f"<i>Продолжая, вы принимаете\n"
                               f"<a href='...'>Пользовательское соглашение</a> "
                               f"и <a href='...'>Политику конфиденциальности</a>.</i>",
                               reply_markup=main_markup
                               )


@main_users_router.message(F.text == '💞Хочу подписку')
async def buy_subscription(message: types.Message) -> None:
    await message.answer(f"(Условия подписки)\n", reply_markup=buy_subscription_markup)


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


@main_users_router.message(F.text == '💘Найти пару')
async def find_couple(message: types.Message) -> None:
    await message.answer(f"{message.from_user.first_name} вы можете перейти в бесплатную группу с анкетами.\n"
                         f"Либо преобрести подписку с анкетами и контактными данными соискателей.\n",
                         reply_markup=go_to_free_chat)
