import logging
import sqlite3

logger = logging.getLogger(__name__)


class DatabaseConnect:
    def __init__(self, path_to_db="data/db_bot.db"):
        self.path_to_db = path_to_db

    @property
    def connect(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self,
                sql: str,
                parameters: tuple = None,
                fetchall=False,
                fetchone=False,
                commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connect
        connection.set_trace_callback(logger_bd)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data


def logger_bd(stattement):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info(f"""
    ________________________________________
    Executing:
    {stattement}
    ________________________________________
    """)
