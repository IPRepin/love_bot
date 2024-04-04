import logging
import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()


class DatabaseConnect:
    def __init__(self, path_to_db=os.getenv('PATH_TO_DB')):
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
        with connection:
            cursor.execute(sql, parameters)
            if commit:
                connection.commit()
            if fetchone:
                data = cursor.fetchone()
            if fetchall:
                data = cursor.fetchall()
        return data


def logger_bd(stattement):
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info(f"""
    ________________________________________
    Executing:
    {stattement}
    ________________________________________
    """)
