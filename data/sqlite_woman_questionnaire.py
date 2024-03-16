from data.sqlite_connect import DatabaseConnect


class WomanQuestionnaires(DatabaseConnect):

    def create_table_women_questionnaires(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Womansqensquestionnaires (
          user_id INTEGER NOT NULL,
          photo VARCHAR(255) NOT NULL,
          user_name VARCHAR(100) NOT NULL,
          user_url VARCHAR(255) NOT NULL,
          gender VARCHAR(50) NOT NULL,
          age INTEGER NOT NULL,
          about_me TEXT NOT NULL,
          finding VARCHAR(50) NOT NULL,
          status VARCHAR(10) NOT NULL,
          moderation BOOLEAN,
          PRIMARY KEY (user_id)
        );"""
        self.execute(sql, commit=True)

    def add_profile(self, user_id, photo, user_name, user_url, gender, age, about_me, finding, status, moderation=None):
        sql = ("INSERT INTO Womansqensquestionnaires (user_id, photo, user_name, user_url, gender, age,"
               " about_me, finding, status, moderation)"
               " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        parameters = (user_id, photo, user_name, user_url, gender, age, about_me, finding, status, moderation)
        self.execute(sql, parameters, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f" {item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def profile_exists(self, user_id):
        sql = "SELECT * FROM Womansqensquestionnaires WHERE user_id = ?"
        parameters = tuple([user_id])
        return bool(self.execute(sql, parameters, fetchone=True))

    def select_profile(self, **kwargs):
        sql = "SELECT * FROM Womansqensquestionnaires WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def delete_profile(self, **kwargs) -> None:
        sql = "DELETE FROM Womansqensquestionnaires WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, commit=True)
