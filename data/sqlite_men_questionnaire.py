from data.sqlite_connect import DatabaseConnect


class MensQuestionnaires(DatabaseConnect):

    def create_table_men_questionnaires(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Mensquestionnaires (
          user_id INTEGER NOT NULL,
          photo VARCHAR(255) NOT NULL,
          user_name VARCHAR(100) NOT NULL,
          user_url VARCHAR(255) NOT NULL,
          gender VARCHAR(50) NOT NULL,
          age INTEGER NOT NULL,
          about_me VARCHAR(255) NOT NULL,
          finding VARCHAR(50) NOT NULL,
          social_network VARCHAR(50) NOT NULL,
          moderation varchar(50),
          PRIMARY KEY (user_id)
        );"""
        self.execute(sql, commit=True)

    def add_profile(self, user_id, photo, user_name, user_url, gender, age, about_me, finding,
                    social_network, moderation="Не промодерировано"):
        sql = ("INSERT INTO Mensquestionnaires (user_id, photo, user_name, user_url, gender, age,"
               " about_me, finding, social_network, moderation)"
               " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        parameters = (user_id, photo, user_name, user_url, gender, age, about_me, finding,
                      social_network, moderation)
        self.execute(sql, parameters, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f" {item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def profile_exists(self, user_id):
        sql = "SELECT * FROM Mensquestionnaires WHERE user_id = ?"
        parameters = tuple([user_id])
        return bool(self.execute(sql, parameters, fetchone=True))

    def select_all(self):
        sql = "SELECT * FROM Mensquestionnaires"
        return self.execute(sql, fetchall=True)

    def select_profile(self, **kwargs):
        sql = "SELECT * FROM Mensquestionnaires WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def delete_profile(self, **kwargs) -> None:
        sql = "DELETE FROM Mensquestionnaires WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, commit=True)

    def update_moderation(self, moderation: str, user_id: int) -> None:
        sql = "UPDATE Mensquestionnaires SET moderation=? WHERE user_id=?"
        return self.execute(sql, parameters=(moderation, user_id), commit=True)
