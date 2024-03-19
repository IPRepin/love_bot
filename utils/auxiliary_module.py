'''
Модуль содержит дополнительный функционал для работы с ботом
'''


def administrator_text(data: dict) -> str:
    '''
    Функция формирует текст для администратора
    '''
    form_msg = []
    [
        form_msg.append(f'{key}: {value}')
        for key, value in data.items()
    ]
    return "\n".join(form_msg[2:])


def moderator_text(data: list) -> str:
    return (f"user_id: {data[0]}\n"
            f"name: {data[2]}\n"
            f"sex: {data[3]}\n"
            f"age: {data[4]}\n"
            f"user_url: {data[5]}\n"
            f"about_me: {data[6]}\n"
            f"status: {data[7]}\n"
            )
