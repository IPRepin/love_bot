import asyncio
import logging

from aiogram import types, Router, F, Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from data.sqlite_db_users import DatabaseUsers
from filters.admins_filter import AdminsFilter, admins_filter
from keyboards.inline import (mail_users_keyboard,
                              get_confirm_button,
                              add_mailing_button,
                              confirm_maling_button)
from keyboards.replay import admin_markup
from pydantic import ValidationError
from utils.logs_hendler_telegram import TelegramBotHandler
from utils.states import MailingState

mailing_router = Router()
db_users = DatabaseUsers()

logger = logging.getLogger(__name__)
telegram_log_handler = TelegramBotHandler()
logging.basicConfig(
    handlers=logger.addHandler(telegram_log_handler),
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@mailing_router.message(F.text == '📨Отправить рассылку',
                        AdminsFilter(admins_filter()),
                        )
async def get_mailing(message: types.Message,
                      state: FSMContext):
    await message.answer("Кому хотим отправить рассылку?", reply_markup=mail_users_keyboard)
    await state.set_state(MailingState.CALL_MAILING)


@mailing_router.callback_query(
    F.data.in_(['send_all_users',
                'send_questionnaire_users',
                'send_no_questionnaire_users',
                "send_deleted_questionnaire",
                ], ),
    AdminsFilter(admins_filter()),
    MailingState.CALL_MAILING,
)
async def send_all_users(call: types.CallbackQuery,
                         state: FSMContext):
    await state.update_data(call=call.data)
    await state.set_state(MailingState.MAIL_TEXT)
    await call.message.answer("Добавьте текст к рассылке")
    await call.answer()


@mailing_router.message(MailingState.MAIL_TEXT)
async def add_button_choice(message: types.Message, state: FSMContext):
    await state.update_data(mailing_text=message.text,
                            message_id=message.message_id,
                            chat_id=message.from_user.id)
    await state.set_state(MailingState.ADD_BUTTON)
    await message.answer("Добавьте кнопку к рассылке",
                         reply_markup=get_confirm_button())


@mailing_router.callback_query(MailingState.ADD_BUTTON,
                               F.data.in_(['add_mailing_button',
                                           'no_mailing_button',
                                           ], ),
                               )
async def add_button_mailing(call: types.CallbackQuery,
                             state: FSMContext,
                             ):
    if call.data == 'add_mailing_button':
        await call.message.answer("Введи текст кнопки, например\n"
                                  "🤗Подписаться", reply_markup=None)
        await state.set_state(MailingState.BUTTON_TEXT)
    elif call.data == 'no_mailing_button':
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer("Добавь фото к рассылке")
        await state.set_state(MailingState.ADD_MEDIA)
    await call.answer()


@mailing_router.message(MailingState.BUTTON_TEXT)
async def get_text_button(message: types.Message, state: FSMContext):
    await state.update_data(button_text=message.text)
    await message.answer("Теперь добавь ссылку для кнопки, например\n"
                         "https://ya.ru/",
                         disable_web_page_preview=True)
    await state.set_state(MailingState.BUTTON_URL)


@mailing_router.message(MailingState.BUTTON_URL)
async def get_url_button(message: types.Message, state: FSMContext):
    await state.update_data(button_url=message.text)
    await state.set_state(MailingState.ADD_MEDIA)
    await message.answer("Добавь фото к рассылке")


async def confirm(
        message: types.Message,
        bot: Bot,
        photo_id: str,
        message_text: str,
        chat_id: int,
        reply_markup: InlineKeyboardMarkup = None,
):
    await bot.send_photo(chat_id=chat_id,
                         photo=photo_id,
                         caption=message_text,
                         reply_markup=reply_markup)
    await message.answer("Вот рассылка которая будет оправлена\n"
                         "Подтвердить отрпавку.",
                         reply_markup=confirm_maling_button
                         )


@mailing_router.message(MailingState.ADD_MEDIA, F.photo)
async def sending_mailing(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    message_text = data.get("mailing_text")
    chat_id = int(data.get("chat_id"))
    photo_id = data.get("photo")
    await confirm(message=message,
                  bot=bot,
                  photo_id=photo_id,
                  message_text=message_text,
                  chat_id=chat_id)


async def send_mails(call_users: str,
                     photo: str,
                     mailing_text: str,
                     bot: Bot,
                     button_message
                     ):
    all_users = ''
    if call_users == "send_all_users":
        all_users = [user[0] for user in db_users.select_all_user_by_id()]
    elif call_users == "send_questionnaire_users":
        all_users = [user[0] for user in
                     db_users.select_all_users_by_params(questionnaire="ЕСТЬ")]
    elif call_users == "send_no_questionnaire_users":
        all_users = [user[0] for user in
                     db_users.select_all_users_by_params(questionnaire="НЕТ")]
    elif call_users == "send_deleted_questionnaire":
        all_users = [user[0] for user in
                     db_users.select_all_users_by_params(questionnaire="УДАЛЕНА")]
    for user in all_users:
        try:
            await bot.send_photo(chat_id=user,
                                 photo=photo,
                                 caption=mailing_text,
                                 reply_markup=button_message)
            await asyncio.sleep(0.5)
        except TelegramRetryAfter as e:
            logger.error(e)
            await asyncio.sleep(e.retry_after)
            await bot.send_photo(chat_id=user,
                                 photo=photo,
                                 caption=mailing_text,
                                 reply_markup=button_message)


@mailing_router.callback_query(
    F.data.in_(['confirm_mailing',
                'cancel_mailing',
                ], ),
)
async def sender_mailing(
        call: types.CallbackQuery,
        bot: Bot,
        state: FSMContext,
):
    if call.data == 'confirm_mailing':
        data = await state.get_data()
        await state.clear()
        call_users = data.get("call")
        photo = data.get('photo')
        mailing_text = data.get('mailing_text')
        button_text = data.get('button_text')
        button_url = data.get('button_url')
        try:
            button_message = add_mailing_button(
                text_button=button_text,
                url_button=button_url,
            )
        except ValidationError as error:
            logger.info(error)
            button_message = None
        try:
            await call.message.answer("К сожалению телеграм имеет ограничения "
                                      "на отправку сообщений "
                                      "поэтому отправка может занять определенное время.\n"
                                      "Дождитесь уведомления об успешной отправке")
            await send_mails(
                call_users,
                photo,
                mailing_text,
                bot,
                button_message
            )
            await call.message.answer("Рассылка отправлена")
        except TelegramBadRequest as e:
            logger.error(e)
            await call.message.answer(f"Ошибка при отправке рассылки {e}"
                                      ",\nпопробуйте создать новую рассылку",
                                      reply_markup=admin_markup)
    else:
        await state.clear()
        await call.message.answer("Вы отменили рассылку")
    await call.answer()
    await call.message.answer("Главное меню", reply_markup=admin_markup)


@mailing_router.message(MailingState.ADD_MEDIA, ~F.photo)
async def incorrect_mailing_photo(message: types.Message, state: FSMContext) -> None:
    await message.answer("Нужно загрузить фотографию!")


