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
from hendlers.hendler_commands import router_commands
from hendlers.states_man import men_questionnaires_router
from hendlers.states_woman import woman_questionnaires_router
from hendlers.user_hendlers import main_users_router
from utils.commands import register_commands
from utils.logs_hendler_telegram import TelegramBotHandler

logger = logging.getLogger(__name__)


def create_tables():
    db_users = DatabaseUsers()
    db_man_questionnaires = MensQuestionnaires()
    db_woman_questionnaires = WomanQuestionnaires()
    try:
        db_users.create_table_users()
        db_man_questionnaires.create_table_men_questionnaires()
        db_woman_questionnaires.create_table_women_questionnaires()
        logger.info("Tables created")
    except Exception as e:
        logger.error(e)


async def connect_telegram():
    storage = RedisStorage.from_url("redis://localhost:6379/0")
    bot = Bot(token=telegram_token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)
    dp.include_routers(router_commands,
                       men_questionnaires_router,
                       woman_questionnaires_router,
                       main_users_router,
                       )
    create_tables()
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        await register_commands(bot)
    except TelegramNetworkError as te:
        logger.error(te)
    finally:
        await bot.close()


if __name__ == '__main__':
    load_dotenv()
    telegram_log_handler = TelegramBotHandler()
    logging.basicConfig(
        handlers=[telegram_log_handler],
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    try:
        asyncio.run(connect_telegram())
    except TelegramRetryAfter as error:
        logger.error(error)
    except KeyboardInterrupt:
        logger.info('Bot interrupted')
