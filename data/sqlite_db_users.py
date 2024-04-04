import logging

from data.sqlite_connect import DatabaseConnect
from utils.logs_hendler_telegram import TelegramBotHandler

logger = logging.getLogger(__name__)
telegram_log_handler = TelegramBotHandler()
logging.basicConfig(
    handlers=logger.addHandler(telegram_log_handler),
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class DatabaseUsers(DatabaseConnect):

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
          user_name VARCHAR(255) NOT NULL,
          user_id INTEGER NOT NULL,
          user_url VARCHAR(255),
          questionnaire VARCHAR(255) NOT NULL,
          PRIMARY KEY (user_id)
        );"""
        self.execute(sql, commit=True)

    def add_user(self,
                 user_id: int,
                 user_name: str,
                 user_url: str = None,
                 questionnaire: str = "НЕТ",
                 ):
        sql = "INSERT INTO Users (user_id, user_name, user_url, questionnaire) VALUES (?,?,?,?)"
        parameters = (user_id, user_name, user_url, questionnaire,)
        self.execute(sql, parameters, commit=True)

    def availability_questionnaire(self, questionnaire: str, user_id: int):
        sql = "UPDATE Users SET questionnaire=? WHERE user_id=?"
        return self.execute(sql, parameters=(questionnaire, user_id), commit=True)

    def user_exists(self, user_id):
        sql = "SELECT * FROM Users WHERE user_id = ?"
        parameters = tuple([user_id])
        return bool(self.execute(sql, parameters, fetchone=True))

    def select_all_users(self):
        sql = "SELECT * FROM Users;"
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f" {item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE")

    def delete_user(self, user_id):
        sql = "DELETE FROM Users WHERE user_id = ?"
        parameters = tuple([user_id])
        return self.execute(sql, parameters, commit=True)

    def select_all_user_by_id(self):
        sql = "SELECT user_id FROM Users"
        return self.execute(sql, fetchall=True)

    def select_all_users_by_params(self, **kwargs):
        sql = "SELECT user_id FROM Users WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)
