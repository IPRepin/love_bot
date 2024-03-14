import logging
import sqlite3

from aiogram import types, Router, F
from aiogram.filters import CommandStart

from data.sqlite_db_users import DatabaseUsers
from keyboards.replay import main_markup, edit_man_profile_markup, edit_woman_profile_markup

from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires

router_commands = Router()
db_men = MensQuestionnaires()
db_woman = WomanQuestionnaires()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@router_commands.message(CommandStart())
async def get_start(message: types.Message) -> None:

    try:
        DatabaseUsers().add_user(
            user_id=message.from_user.id,
            user_name=message.from_user.first_name,
            user_url=message.from_user.url
        )
        await message.answer(f"Привет {message.from_user.first_name}😄\n"
                             f"Давай начнем знакомство?\n"
                             f"\n"
                             f"<i>Продолжая, вы принимаете:\n"
                             f"<a href='https://ya.ru'>Пользовательское соглашение</a>\n"
                             f"и <a href='https://ya.ru'>Политику конфиде нциальности</a>.</i>",
                             reply_markup=main_markup
                             )
    except (sqlite3.IntegrityError, sqlite3.OperationalError) as err:
        logger.error(err)
        logger.error("Пользователь с таким id уже существует")
        if db_men.profile_exists(user_id=message.from_user.id):
            await message.answer(f"С возвращением {message.from_user.first_name}\n"
                                 f"Ты уже заполнил анкету анкету❓\n"
                                 f"\n"
                                 f"<i>Продолжая, вы принимаете:\n"
                                 f"<a href='...'>Пользовательское соглашение</a> "
                                 f"и <a href='...'>Политику конфиденциальности</a>.</i>",
                                 reply_markup=edit_man_profile_markup
                                 )
        elif db_men.profile_exists(user_id=message.from_user.id):
            await message.answer(f"С возвращением {message.from_user.first_name}\n"
                                 f"Ты уже заполнил анкету анкету❓\n"
                                 f"\n"
                                 f"<i>Продолжая, вы принимаете:\n"
                                 f"<a href='...'>Пользовательское соглашение</a> "
                                 f"и <a href='...'>Политику конфиденциальности</a>.</i>",
                                 reply_markup=edit_woman_profile_markup
                                 )
        else:
            await message.answer(f"С возвращением {message.from_user.first_name}\n"
                                 f"У тебя нет  анкеты❓\n"
                                 f"\n"
                                 f"<i>Продолжая, вы принимаете:\n"
                                 f"<a href='...'>Пользовательское соглашение</a> "
                                 f"и <a href='...'>Политику конфиденциальности</a>.</i>",
                                 reply_markup=main_markup
                                 )


@router_commands.message(F.text == '/help')
async def help_command(message: types.Message) -> None:
    await message.answer(f"- /start - Начать заполнение анкеты;\n")
