"""Функции обработки кнопок основного меню"""

from aiogram import types, Router, F

main_users_router = Router()


@main_users_router.callback_query(F.data == 'men_gender')
async def man_users_gender(query: types.CallbackQuery):
    await query.message.edit_text("Парень")

