"""Функции обработки кнопок основного меню"""

from aiogram import types, Router, F

from keyboards.inline import buy_subscription_markup
from keyboards.replay import main_markup

main_users_router = Router()


@main_users_router.callback_query(F.data == 'cancel')
async def man_users_gender(query: types.CallbackQuery):
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
