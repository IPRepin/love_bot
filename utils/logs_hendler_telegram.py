'''
Модуль отправки логов в Telegram
'''
import urllib3
import logging
import os
from datetime import datetime
from logging import LogRecord, Handler
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()


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


def setup_bot_logger():
    logging.basicConfig(level=logging.INFO)
    logs_path = os.getenv('LOGS_PATH')
    if not logs_path:
        logs_path = "logs"
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    dt_now = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{logs_path}/{dt_now}_bot.log"
    log_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=5)
    bot_hanndler = TelegramBotHandler()

    formatter = logging.Formatter('%(asctime)s - love_bot -  %(name)s'
                                  ' - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    bot_hanndler.setFormatter(formatter)
    logging.getLogger().addHandler(log_handler)
    logging.getLogger().addHandler(bot_hanndler)

# TODO добавить логирование ошибок
