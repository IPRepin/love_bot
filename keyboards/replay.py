from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='🙋‍♂️Заполнить мужскую анкету'),
    ],
    [
        KeyboardButton(text='🙋‍♀️Заполнить женскую анкету'),
    ],
], resize_keyboard=True, input_field_placeholder="Начни с заполнения анкеты⬇️", one_time_keyboard=True)