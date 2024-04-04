import logging

from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from pydantic import ValidationError

from data.sqlite_db_users import DatabaseUsers
from filters.admins_filter import AdminsFilter, admins_filter
from keyboards.inline import (mail_users_keyboard,
                              get_confirm_button,
                              add_mailing_button,
                              confirm_maling_button)
from keyboards.replay import admin_markup
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
                                  "'🤗Подписаться'", reply_markup=None)
        await state.set_state(MailingState.BUTTON_TEXT)
    elif call.data == 'no_mailing_button':
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer("Добавь фото к рассылке")
        await state.set_state(MailingState.ADD_PHOTO)
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
    await state.set_state(MailingState.ADD_PHOTO)
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
    await message.answer("Вот рассылка которая будет оправлена"
                         "Подтвердить отрпавку.",
                         reply_markup=confirm_maling_button
                         )


@mailing_router.message(MailingState.ADD_PHOTO, F.photo)
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
            logger.error(error)
            button_message = None
        if call_users == "send_all_users":
            all_users = [user[0] for user in db_users.select_all_user_by_id()]
            for user in all_users:
                await bot.send_photo(user, photo, caption=mailing_text, reply_markup=button_message)
        elif call_users == "send_questionnaire_users":
            questionnaire_users = [user[0] for user in db_users.select_all_users_by_params(questionnaire="ЕСТЬ")]
            for user in questionnaire_users:
                await bot.send_photo(user, photo, caption=mailing_text, reply_markup=button_message)
        elif call_users == "send_no_questionnaire_users":
            questionnaire_users = [user[0] for user in db_users.select_all_users_by_params(questionnaire="НЕТ")]
            for user in questionnaire_users:
                await bot.send_photo(user, photo, caption=mailing_text, reply_markup=button_message)
        elif call_users == "send_deleted_questionnaire":
            questionnaire_users = [user[0] for user in db_users.select_all_users_by_params(questionnaire="УДАЛЕНА")]
            for user in questionnaire_users:
                await bot.send_photo(user, photo, caption=mailing_text, reply_markup=button_message)
    else:
        await state.clear()
        await call.message.answer("Вы отменили рассылку")
    await call.answer()
    await call.message.answer("Главное меню", reply_markup=admin_markup)
# TODO сделать функции проверок контекта, добавить паузу между сообщениями
# TODO выявить и обработать исключения
