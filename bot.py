import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv

from data.sqlite_db_users import DatabaseUsers
from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires
from hendlers.admin_hendlers import main_admin_router
from hendlers.admin_mailing_handler import mailing_router
from hendlers.download_hendlers import download_router
from hendlers.hendler_commands import router_commands
from hendlers.states_man import men_questionnaires_router
from hendlers.states_woman import woman_questionnaires_router
from hendlers.user_hendlers import main_users_router
from utils.commands import register_commands
from utils.logs_hendler_telegram import setup_bot_logger


def create_tables():
    try:
        db_users.create_table_users()
        db_man_questionnaires.create_table_men_questionnaires()
        db_woman_questionnaires.create_table_women_questionnaires()
        logger.info("Tables created")
    except Exception as err:
        logger.exception(err)


async def connect_telegram():
    storage = RedisStorage.from_url("redis://localhost:6379/0")
    bot = Bot(token=telegram_token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)
    dp.include_routers(router_commands,
                       men_questionnaires_router,
                       woman_questionnaires_router,
                       main_users_router,
                       main_admin_router,
                       download_router,
                       mailing_router,
                       )
    create_tables()
    try:
        await bot.delete_webhook(drop_pending_updates=False)
        await dp.start_polling(bot)
        await register_commands(bot)
    except TelegramNetworkError as telegram_err:
        logger.exception(telegram_err)
    finally:
        await bot.close()


if __name__ == '__main__':
    load_dotenv()
    setup_bot_logger()
    logger = logging.getLogger(__name__)
    db_users = DatabaseUsers()
    db_man_questionnaires = MensQuestionnaires()
    db_woman_questionnaires = WomanQuestionnaires()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    try:
        logger.info("Bot started")
        asyncio.run(connect_telegram())
    except TelegramRetryAfter as retry_error:
        logger.error(retry_error)
    except KeyboardInterrupt:
        logger.error('Bot interrupted')
