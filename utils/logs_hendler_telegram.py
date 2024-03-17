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


# def setup_logger():
#     logger_handler = logging.getLogger(__name__)
#     telegram_log_handler = TelegramBotHandler()
#     logging.basicConfig(
#         handlers=logger_handler.addHandler(telegram_log_handler),
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     return logger_handler
