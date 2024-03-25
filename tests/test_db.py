'''
Модульное тестирование базы данных sqlite3
'''


def test_insert_db_user(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO Users (user_name, user_id, user_url) VALUES ('Bob', 30, '@bob')")
    db_connection.commit()
    cursor.execute("SELECT * FROM Users WHERE user_name='Bob'")
    result = cursor.fetchone()
    assert result is not None


def test_update_record(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO Users (user_name, user_id, user_url) VALUES ('Bob', 30, '@bob')")
    db_connection.commit()
    cursor.execute("UPDATE Users SET user_name='David' WHERE user_id=30")
    db_connection.commit()
    cursor.execute("SELECT * FROM Users WHERE user_id=30")
    result = cursor.fetchone()
    assert result[0] == "David"


def test_column_type(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('PRAGMA table_info(Users)')
    columns = cursor.fetchall()
    for column in columns:
        if column[1] == 'user_name':
            assert column[2] == 'VARCHAR(255)'
        elif column[1] == 'user_id':
            assert column[2] == 'INTEGER'
        elif column[1] == 'user_url':
            assert column[2] == 'VARCHAR(255)'


def test_null_value(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO Users (user_name, user_id, user_url) VALUES (NULL, 30, '@bob')")
    db_connection.commit()
    cursor.execute("SELECT * FROM Users WHERE user_name IS NULL")
    result = cursor.fetchone()
    assert result is not None


def test_delete_record(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO Users (user_name, user_id, user_url) VALUES ('Bob', 30, '@bob')")
    db_connection.commit()
    cursor.execute("DELETE FROM Users WHERE user_name='Bob'")
    db_connection.commit()
    cursor.execute("SELECT * FROM Users WHERE user_name='Bob'")
    result = cursor.fetchone()
    assert result is None
