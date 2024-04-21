'''
Модуль отправки логов в Telegram
'''
import logging
import os
from logging import LogRecord, Handler

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
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )




#TODO добавить логирование ошибок
