from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton

channel_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="↩️На главное меню", callback_data="cancel")],
    ]
)

buy_subscription_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🤩Преобрести подписку",
                url="https://t.me/+eri-YbFPwbY1OWVi",
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

go_to_free_chat = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🆓Перейти в беслатную группу",
                url='https://t.me/znakm100'
            )
        ],
        [
            InlineKeyboardButton(
                text="🤩Преобрести подписку",
                url="https://t.me/+eri-YbFPwbY1OWVi",
            )
        ],
        # [InlineKeyboardButton(text="↩️На главное меню", callback_data="back")],
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
