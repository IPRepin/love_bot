import logging
import os

from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from data.sqlite_db_users import DatabaseUsers
from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires
from filters.admins_filter import AdminsFilter
from keyboards.inline import moderation_keyboard, download_button
from utils.auxiliary_module import moderator_text
from utils.states import UserIdState

logger = logging.getLogger(__name__)
load_dotenv()
db_men = MensQuestionnaires()
db_woman = WomanQuestionnaires()
db_users = DatabaseUsers()
main_admin_router = Router()


@main_admin_router.callback_query(F.data == 'approved' or F.data == 'rejected',
                                  AdminsFilter([int(os.getenv("ADMINS_ID"))]),
                                  UserIdState.USER_ID
                                  )
async def moderation_questionnaires(query: types.CallbackQuery,
                                    bot: Bot,
                                    state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    user_id = data.get('user_id')
    logger.info(f'user_id: {user_id}')
    if query.data == 'approved' and db_men.profile_exists(user_id=user_id):
        db_men.update_moderation(user_id=user_id, moderation='Одобрено')
        await query.message.answer("✅Анкета одобрена, пользователю отправлено"
                                   "уведомление о результате проверки")
        await query.answer()
        await bot.send_message(chat_id=user_id, text="✅Ваша анкета одобрена")
    elif query.data == 'approved' and db_woman.profile_exists(user_id=user_id):
        db_woman.update_moderation(user_id=user_id, moderation='Одобрено')
        await query.message.answer("✅Анкета одобрена, пользователю отправлено"
                                   "уведомление о результате проверки")
        await bot.send_message(chat_id=user_id, text="✅Ваша анкета одобрена")
        await query.answer()
    elif query.data == 'rejected' and db_men.profile_exists(user_id=user_id):
        db_men.update_moderation(user_id=user_id, moderation='Отклонено')
        await query.message.answer("🚫Анкета отклонена, пользователю отправлено"
                                   "уведомление о результате проверки")
        await bot.send_message(chat_id=user_id,
                               text="🚫Ваша анкета отклонена\n"
                                    "Вы можете отправить новую анкету нажав на кнопку ниже\n"
                                    "✏️Отредактировать анкету")
        await query.answer()
    elif query.data == 'rejected' and db_woman.profile_exists(user_id=user_id):
        db_woman.update_moderation(user_id=user_id, moderation='Отклонено')
        await query.message.answer("🚫Анкета отклонена, пользователю отправлено"
                                   "уведомление о результате проверки")
        await bot.send_message(chat_id=user_id,
                               text="🚫Ваша анкета отклонена\n"
                                    "Вы можете отправить новую анкету нажав на кнопку ниже\n"
                                    "✏️Отредактировать анкету")
        await query.answer()


@main_admin_router.callback_query(F.data.in_(['approved', 'rejected']),
                                  AdminsFilter([int(os.getenv("ADMINS_ID"))]),
                                  )
async def not_moderation_questionnaires(query: types.CallbackQuery):
    await query.message.answer("Анкета уже проверена, либо пользователь удалил анкету!")
    await query.answer()


@main_admin_router.message(F.text == "⏩Проверить анкеты",
                           AdminsFilter([int(os.getenv("ADMINS_ID"))]), )
async def next_moderation_questionnaires(message: types.Message,
                                         state: FSMContext,
                                         bot: Bot) -> None:
    if db_men.select_profile(moderation="Не промодерировано"):
        questionnaires = db_men.select_profile(moderation="Не промодерировано")
        await state.set_state(UserIdState.USER_ID)
        await state.update_data(user_id=int(questionnaires[0]))
        await bot.send_photo(chat_id=message.chat.id, photo=questionnaires[1],
                             caption=moderator_text(questionnaires),
                             reply_markup=moderation_keyboard,
                             )
    elif db_woman.select_profile(moderation="Не промодерировано"):
        questionnaires = db_woman.select_profile(moderation="Не промодерировано")
        await state.set_state(UserIdState.USER_ID)
        await state.update_data(user_id=int(questionnaires[0]))
        await bot.send_photo(chat_id=message.chat.id, photo=questionnaires[1],
                             caption=moderator_text(questionnaires),
                             reply_markup=moderation_keyboard,
                             )
    else:
        await message.answer("😎Все анкеты проверены!")


@main_admin_router.message(F.text == '💾Выгрузить данные пользователей',
                           AdminsFilter([int(os.getenv("ADMINS_ID"))]),
                           )
async def get_questionnaires(message: types.Message) -> None:
    await message.answer("Можно выгрузить всех пользователей бота (не анкеты).\n"
                         "Либо анкеты пользоветелей.",
                         reply_markup=download_button)
