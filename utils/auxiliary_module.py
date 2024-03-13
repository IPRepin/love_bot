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
    return "\n".join(form_msg[1:])
