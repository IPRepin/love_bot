import logging
import os
import sqlite3

from aiogram import types, Router, F
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from data.sqlite_db_users import DatabaseUsers
from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires
from keyboards.replay import main_markup, edit_profile_markup

load_dotenv()
logger = logging.getLogger(__name__)
router_commands = Router()
db_men = MensQuestionnaires()
db_woman = WomanQuestionnaires()


@router_commands.message(CommandStart())
async def get_start(message: types.Message) -> None:
    try:
        if str(message.from_user.id) not in os.environ.get("ADMINS_ID").split(","):
            logger.info(os.environ.get("ADMINS_ID").split(","))
            DatabaseUsers().add_user(
                user_id=message.from_user.id,
                user_name=message.from_user.first_name,
                user_url=message.from_user.username,
            )
            await message.answer(f"Привет {message.from_user.first_name}👋\n"
                                 f"Давай начнем знакомство?\n"
                                 f"\n"
                                 f"<i>Продолжая, вы принимаете:\n"
                                 f"<a href='...'>Пользовательское соглашение</a>"
                                 f" и <a href='...'>Политику конфиде нциальности</a>.</i>",
                                 reply_markup=main_markup,
                                 disable_web_page_preview=True,
                                 )
        else:
            await message.answer(f"{message.from_user.first_name} вы являетесь администратором бота.\n"
                                 f"В этот чат вам будут приходить анкеты пользователей.")
    except (sqlite3.IntegrityError, sqlite3.OperationalError) as err:
        logger.error(err)
        logger.error("Пользователь с таким id уже существует")
        if db_men.profile_exists(user_id=message.from_user.id):
            await message.answer(f"С возвращением {message.from_user.first_name}\n"
                                 f"✅Ты уже заполнил анкету анкету.\n"
                                 f"\n"
                                 f"<i>Продолжая, вы принимаете:\n"
                                 f"<a href='...'>Пользовательское соглашение</a> "
                                 f"и <a href='...'>Политику конфиденциальности</a>.</i>",
                                 reply_markup=edit_profile_markup,
                                 disable_web_page_preview=True,
                                 )
        elif db_woman.profile_exists(user_id=message.from_user.id):
            await message.answer(f"С возвращением {message.from_user.first_name}\n"
                                 f"✅Ты уже заполнила анкету анкету.\n"
                                 f"\n"
                                 f"<i>Продолжая, вы принимаете:\n"
                                 f"<a href='...'>Пользовательское соглашение</a> "
                                 f"и <a href='...'>Политику конфиденциальности</a>.</i>",
                                 reply_markup=edit_profile_markup,
                                 disable_web_page_preview=True,
                                 )
        else:
            await message.answer(f"С возвращением {message.from_user.first_name}\n"
                                 f"У тебя нет до сих пор анкеты😟\n"
                                 f"Давай заполним?"
                                 f"\n"
                                 f"<i>Продолжая, вы принимаете:\n"
                                 f"<a href='...'>Пользовательское соглашение</a> "
                                 f"и <a href='...'>Политику конфиденциальности</a>.</i>",
                                 reply_markup=main_markup,
                                 disable_web_page_preview=True,
                                 )


@router_commands.message(F.text == '/help')
async def help_command(message: types.Message) -> None:
    await message.answer(f"- /start - Начать заполнение анкеты;\n")
