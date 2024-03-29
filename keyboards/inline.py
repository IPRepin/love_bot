import os
from dotenv import load_dotenv

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton

load_dotenv()

channel_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],
    ]
)

buy_subscription_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🤩Оформить подписку",
                url=os.environ.get("BUY_CHANNEL"),
            )
        ],
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],

    ]
)

confirmation_of_deletion = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да удалить", callback_data="delete")],
        [InlineKeyboardButton(text="Не удалять", callback_data="cancel")],
    ]
)

send_video = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📽Отправить видео",
                              url=os.getenv("VIDEO_CHANNEL"))],
    ]
)

moderation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅Одобрено", callback_data="approved")],
        [InlineKeyboardButton(text="🚫Отклонено", callback_data="rejected")],
    ]
)

download_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Скачать пользователей бота", callback_data="all_users")
        ],
        [
            InlineKeyboardButton(text="Скачать мужские анкеты", callback_data="male_users"),
        ],
        [
            InlineKeyboardButton(text="Скачать женские анкеты", callback_data="female_users"),
        ]
    ],
)

sub_check_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👉ПОДПИСАТСЯ", url=os.getenv('TG_CHANNEL_URL'))],
        [InlineKeyboardButton(text="✅Я ПОДПИСАЛСЯ", callback_data="check_channel")]
    ]
)