'''
Модуль содержит дополнительный функционал для работы с ботом
'''
import csv
from datetime import datetime


def administrator_text(data: dict) -> str:
    '''
    Функция формирует текст для администратора
    '''
    form_msg = []
    [
        form_msg.append(f'{key}: {value}')
        for key, value in data.items()
    ]
    return "\n".join(form_msg[1:])


def moderator_text(data: list) -> str:
    return (f"user_id: {data[0]}\n"
            f"Имя: {data[2]}\n"
            f"user_url: {data[3]}\n"
            f"Пол: {data[4]}\n"
            f"Возраст: {data[5]}\n"
            f"Обо мне: {data[6]}\n"
            f"Хочу найти: {data[7]}\n"
            f"Связь: {data[8]}\n"
            )


def new_file(data, query):
    name_file = datetime.now().strftime('%d-%m-%Y')
    with open(F'data/{query}_{name_file}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
