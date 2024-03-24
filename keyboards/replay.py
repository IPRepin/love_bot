from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='🙋‍♂️Заполнить мужскую анкету'),
    ],
    [
        KeyboardButton(text='🙋‍♀️Заполнить женскую анкету'),
    ],
    [
        KeyboardButton(text='💞Оформить подписку'),
    ],
], resize_keyboard=True, input_field_placeholder="Начни с заполнения анкеты⬇️", one_time_keyboard=True)

edit_profile_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='✏️Отредактировать анкету'),
    ],
    [
        KeyboardButton(text='🗑️Удалить анкету'),
    ],
], resize_keyboard=True, input_field_placeholder="Отредактировать или удалить анкету⬇️", one_time_keyboard=True)


async def gen_replay_keyboard(text: str | list):
    builder = ReplyKeyboardBuilder()
    if isinstance(text, str):
        text = [text]
    [builder.button(text=txt, callback_data=txt) for txt in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


rmk = ReplyKeyboardRemove()
