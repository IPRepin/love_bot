import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from dotenv import load_dotenv

from data.sqlite_db_users import DatabaseUsers
from data.sqlite_men_questionnaire import MensQuestionnaires
from data.sqlite_woman_questionnaire import WomanQuestionnaires
from hendlers.hendler_commands import router_commands
from utils.commands import register_commands

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
    bot = Bot(token=telegram_token, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(router_commands,
                       )
    create_tables()
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        await register_commands(bot)
    except TelegramNetworkError as error:
        logger.error(error)
    finally:
        await bot.close()


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    try:
        asyncio.run(connect_telegram())
    except KeyboardInterrupt:
        logger.info('Bot interrupted')
