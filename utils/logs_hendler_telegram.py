'''
Модуль отправки логов в Telegram
'''
import logging
import os
from logging import LogRecord, Handler
from logging.handlers import RotatingFileHandler

from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

import urllib3


class TelegramBotHandler(Handler):
    def __init__(self):
        super().__init__()
        self.token = os.getenv('TELEGRAM_LOGS_TOKEN')
        self.chat_id = os.getenv("TG_CHATID_LOGS")

    def emit(self, record: LogRecord) -> None:
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        post_data = {'chat_id': self.chat_id,
                     'text': self.format(record)}
        http = urllib3.PoolManager()
        http.request(method='POST', url=url, fields=post_data)


def setup_bot_logger(name: str):
    logger = logging.getLogger(name)
    logging.basicConfig(
        handlers=logger.addHandler(TelegramBotHandler()),
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logs_pash = os.getenv('LOGS_PASH')
    dt_now = datetime.now()
    dt_now = dt_now.strftime("%Y-%m-%d")
    log_handler = RotatingFileHandler(f'{logs_pash}/{dt_now}bot.log', maxBytes=1e6, backupCount=5)
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)

    logger.addHandler(log_handler)




#TODO добавить логирование ошибок
