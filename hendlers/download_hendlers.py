import asyncio
import logging
import os
from datetime import datetime

from aiogram import types, Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import FSInputFile

from data.sqlite_db_users import DatabaseUsers
from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires
from utils.auxiliary_module import new_file

logger = logging.getLogger(__name__)
db_men = MensQuestionnaires()
db_woman = WomanQuestionnaires()
db_users = DatabaseUsers()
download_router = Router()

#TODO переделать в байты файлы
@download_router.callback_query(F.data == 'all_users')
async def download_all_button(query: types.CallbackQuery,
                              bot: Bot) -> None:
    name_file = datetime.now().strftime('%d-%m-%Y')
    data = db_users.select_all_users()
    new_file(data=data, query='all')
    await asyncio.sleep(6)
    await query.answer()
    file = FSInputFile(F'data/all_{name_file}.csv')
    try:
        await bot.send_document(chat_id=query.message.chat.id,
                                document=file)
        await asyncio.sleep(6)
        os.remove(F'data/all_{name_file}.csv')
        logger.info("Deleted file")
    except TelegramBadRequest as error:
        logger.error(f"В базе данных нет данных\n"
                     f"{error}"
                     )


@download_router.callback_query(F.data == 'male_users')
async def download_male_button(query: types.CallbackQuery,
                               bot: Bot) -> None:
    name_file = datetime.now().strftime('%d-%m-%Y')
    data = db_men.select_all()
    new_file(data=data, query='male')
    await asyncio.sleep(5)
    file = FSInputFile(F'data/male_{name_file}.csv')
    await query.answer()
    try:
        await bot.send_document(chat_id=query.message.chat.id,
                                document=file)
        await asyncio.sleep(5)
        os.remove(F'data/male_{name_file}.csv')
        logger.info("Deleted file")
    except TelegramBadRequest as error:
        logger.error(f"В базе данных нет данных\n"
                     f"{error}"
                     )


@download_router.callback_query(F.data == 'female_users')
async def download_female_button(query: types.CallbackQuery,
                                 bot: Bot) -> None:
    name_file = datetime.now().strftime('%d-%m-%Y')
    data = db_woman.select_all()
    new_file(data=data, query='female')
    await asyncio.sleep(5)
    file = FSInputFile(F'data/female_{name_file}.csv')
    try:
        await bot.send_document(chat_id=query.message.chat.id,
                                document=file)
        await asyncio.sleep(5)
        os.remove(F'data/female_{name_file}.csv')
        logger.info("Deleted file")
    except TelegramBadRequest as error:
        logger.error(f"В базе данных нет данных\n"
                     f"{error}"
                     )
