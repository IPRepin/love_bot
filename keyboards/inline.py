from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


channel_markup = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],
    ]
)
