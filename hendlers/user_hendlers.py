"""Функции обработки кнопок основного меню"""

from aiogram import types, Router, F

from keyboards.replay import main_markup

main_users_router = Router()


@main_users_router.callback_query(F.data == 'cancel')
async def man_users_gender(query: types.CallbackQuery):
    await query.message.answer(f"С возвращением {query.message.from_user.first_name}\n"
                                  f"Хочеш запонить еще одну анкету❓\n"
                                  f"\n"
                                  f"<i>Продолжая, вы принимаете\n"
                                  f"<a href='https://ya.ru'>Пользовательское соглашение</a> "
                                  f"и <a href='https://ya.ru'>Политику конфиденциальности</a>.</i>",
                                  reply_markup=main_markup
                                  )
