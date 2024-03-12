from data.sqlite_connect import DatabaseConnect


class MensQuestionnaires(DatabaseConnect):

    def create_table_men_questionnaires(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Mensquestionnaires (
          user_id INTEGER NOT NULL,
          photo VARCHAR(255) NOT NULL,
          user_name VARCHAR(100) NOT NULL,
          gender VARCHAR(50) NOT NULL,
          age INTEGER NOT NULL,
          about_me VARCHAR(255) NOT NULL,
          finding VARCHAR(50) NOT NULL,
          status VARCHAR(10) NOT NULL,
          moderation VARCHAR(25),
          PRIMARY KEY (user_id)
        );"""
        self.execute(sql, commit=True)

    def add_profile(self, user_id, photo, user_name, gender, age, about_me, finding, status, moderation=None):
        sql = "INSERT INTO Mensquestionnaires (user_id, photo, user_name, gender, age, about_me, finding, status, moderation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        parameters = (user_id, photo, user_name, gender, age, about_me, finding, status, moderation)
        self.execute(sql, parameters, commit=True)
