import os

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()


def get_confirm_button() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Добавить кнопку", callback_data="add_mailing_button")
    keyboard_builder.button(text="Продолжить без кнопки", callback_data="no_mailing_button")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def add_mailing_button(text_button: str, url_button: str) -> InlineKeyboardMarkup:
    added_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=text_button,
                url=url_button
            )]
        ]
    )
    return added_keyboard


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

support_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📨Написать администратору",
                              url=os.getenv("VIDEO_CHANNEL"))],
        [InlineKeyboardButton(text="↩️На главное меню",
                              callback_data="cancel_main")],
    ]
)

mail_users_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="Всем пользователям",
            callback_data="send_all_users"
        )],
        [InlineKeyboardButton(
            text="Пользователям с анкетой",
            callback_data="send_questionnaire_users"
        )],
        [InlineKeyboardButton(
            text="Пользователям без анкеты",
            callback_data="send_no_questionnaire_users"
        )],
        [InlineKeyboardButton(
            text="Тем кто удалил анкету",
            callback_data="send_deleted_questionnaire"
        )],
    ],
)

confirm_maling_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отправить",
                callback_data="confirm_mailing"
            )
        ],
        [InlineKeyboardButton(
            text="Отменить",
            callback_data="cancel_mailing"
        )],
    ])
