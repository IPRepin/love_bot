from data.sqlite_connect import DatabaseConnect


class DatabaseUsers(DatabaseConnect):

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
          user_name VARCHAR(255) NOT NULL,
          user_id INTEGER NOT NULL,
          user_url VARCHAR(255),
          PRIMARY KEY (user_id)
        );"""
        self.execute(sql, commit=True)

    def add_user(self,
                 user_id: int,
                 user_name: str,
                 user_url: str = None,
                 ):
        sql = "INSERT INTO Users (user_id, user_name, user_url) VALUES (?, ?, ?)"
        parameters = (user_id, user_name, user_url)
        self.execute(sql, parameters, commit=True)

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

    def delete_user(self):
        self.execute("DELETE FROM Users WHERE TRUE")
