import logging

from aiogram import types, Router, F, Bot
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from data.sqlite_db_users import DatabaseUsers
from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires
from filters.admins_filter import AdminsFilter, admins_filter
from keyboards.inline import moderation_keyboard, download_button
from utils.auxiliary_module import moderator_text
from utils.logs_hendler_telegram import setup_bot_logger
from utils.states import UserIdState


logger = logging.getLogger(__name__)

load_dotenv()

db_men = MensQuestionnaires()
db_woman = WomanQuestionnaires()
db_users = DatabaseUsers()

main_admin_router = Router()


@main_admin_router.callback_query(F.data.in_(['approved', 'rejected']),
                                  AdminsFilter(admins_filter()),
                                  UserIdState.USER_ID
                                  )
async def moderation_questionnaires(query: types.CallbackQuery,
                                    bot: Bot,
                                    state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    user_id = data.get('user_id')
    logger.info("Moderation questionnaires started")
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
                                    "✏️Отредактировать анкету\n"
                                    "После заполнения анкеты обязательно"
                                    'ОТПРАВЬТЕ ВИДЕОСООБЩЕНИЕ С ФРАЗОЙ "ДЛЯ КАНАЛА ЗНАКОМСТВ"\n'
                                    "НАЖАВ НА КНОПКУ '📽Отправить видео'\n"
                                    "Без этого видео анкета будет отклонена")
        await query.answer()
    elif query.data == 'rejected' and db_woman.profile_exists(user_id=user_id):
        db_woman.update_moderation(user_id=user_id, moderation='Отклонено')
        await query.message.answer("🚫Анкета отклонена, пользователю отправлено"
                                   "уведомление о результате проверки")
        await bot.send_message(chat_id=user_id,
                               text="🚫Ваша анкета отклонена\n"
                                    "Вы можете отправить новую анкету нажав на кнопку ниже\n"
                                    "✏️Отредактировать анкету\n"
                                    "После заполнения анкеты обязательно"
                                    'ОТПРАВЬТЕ ВИДЕОСООБЩЕНИЕ С ФРАЗОЙ "ДЛЯ КАНАЛА ЗНАКОМСТВ"\n'
                                    "НАЖАВ НА КНОПКУ '📽Отправить видео'\n"
                                    "Без этого видео анкета будет отклонена")
        await query.answer()


@main_admin_router.callback_query(F.data.in_(['approved', 'rejected']),
                                  AdminsFilter(admins_filter()),
                                  )
async def not_moderation_questionnaires(query: types.CallbackQuery):
    logger.info("not_moderation_questionnaires")
    await query.message.answer("Анкета уже проверена, либо пользователь удалил анкету!")
    await query.answer()


@main_admin_router.message(F.text == "⏩Проверить анкеты",
                           AdminsFilter(admins_filter()), )
async def next_moderation_questionnaires(message: types.Message,
                                         state: FSMContext,
                                         bot: Bot) -> None:
    try:
        logger.info("next_moderation_questionnaires")
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
    except TelegramNetworkError as telegram_err:
        logger.exception(telegram_err)


@main_admin_router.message(F.text == '💾Выгрузить данные пользователей',
                           AdminsFilter(admins_filter()),
                           )
async def get_questionnaires(message: types.Message) -> None:
    await message.answer("Можно выгрузить всех пользователей бота (не анкеты).\n"
                         "Либо анкеты пользоветелей.",
                         reply_markup=download_button)
