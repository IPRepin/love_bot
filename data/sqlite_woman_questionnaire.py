from data.sqlite_connect import DatabaseConnect


class WomanQuestionnaires(DatabaseConnect):

    def create_table_women_questionnaires(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Womansqensquestionnaires (
          user_id INTEGER NOT NULL,
          photo VARCHAR(255) NOT NULL,
          user_name VARCHAR(100) NOT NULL,
          gender VARCHAR(50) NOT NULL,
          age INTEGER NOT NULL,
          about_me TEXT NOT NULL,
          finding VARCHAR(50) NOT NULL,
          status BOOLEAN NOT NULL,
          moderation VARCHAR(25),
          PRIMARY KEY (user_id)
        );"""
        self.execute(sql, commit=True)

    # def add_questionnaire(self, user_id: int, user_name: str, phone: str,
        #                   ):
        # sql = "INSERT INTO Patient (user_id, user_name, phone) VALUES (?, ?, ?)"
        # parameters = (user_id, user_name, phone)
        # self.execute(sql, parameters, commit=True)
