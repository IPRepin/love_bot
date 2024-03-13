from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton

channel_markup = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],
    ]
)

buy_subscription_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🤩Преобрести подписку",
                url="https://t.me/wallet",
            )
        ],
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],

    ]
)
