# Бот знакомств для Telegram с функцией сбора данных (анкет) пользователей. #

![Static Badge](https://img.shields.io/badge/Python-3.11-blue)
![Static Badge](https://img.shields.io/badge/Aiogram-3.3.0-blue)
![Static Badge](https://img.shields.io/badge/python--dotenv-1.0-blue)
![Static Badge](https://img.shields.io/badge/urllib3-2.2-blue)
![Static Badge](https://img.shields.io/badge/SQLite-3.45.2-blue)
![Static Badge](https://img.shields.io/badge/Redis-5.0.3-blue)


## Описание проекта ##

Бот для Telegram с функцией сбора данных (анкет) пользователей.
Бот предлагает пользователю заполнить анкеты с типовыми вопросами (фото, имя, возраст и т.д). Собранные данные отправляются модератору на
проверку, а также добавляются в базу данных анкет (данные разделяются на мужские и женские анкеты). Также все пользователи вне зависимости от пола
и того заполнили они анкету или нет добавляются в отдельную таблицу базы данных (добавляемые данные: user id телеграм, ссылка в телеграм, first_name).
Есть функция перехода пользователя на преобретение платной подписки без запонения анкеты.
Также имеется возможность отправки сообщений (логов) об ошибках в телеграм.


## Требования к окружению ##

* Python==3.11, 
* aiogram==3.3.0, 
* python-dotenv==1.0.0,
* urllib3==2.2.1
* sqlite == 3.45.2
* redis==5.0.3

## Структура проекта ##

📦love_bot
 * ┣ 📦data _(пакет модулей для работы с БД)_
 * ┣ 📦handlers _(пакет работы с hendlrs бота)_
 * ┣ 📦keyboards _(пакет работы с клавиатурами бота)_
 * ┣ 📦utils _(вспомогательный пакет с дополнительными модулями)_
 * ┣ 📜bot.py _(модуль запуска телеграм бота)_
 * ┣ 📜.gitignore
 * ┗ 📜requirements.txt

## Как установить ##

1. Создаем бота в телеграм при помощи [BotFather](https://t.me/BotFather)
2. Скачиваем репозиторий с ботом при помощи команды: 
   * `git clone https://github.com/IPRepin/love_bot.git`
4. Устанавливаем библиотеки из файла [requirements.txt](https://github.com/IPRepin/love_bot/blob/main/requirements.txt)
5. В корневой папке проекта содаем файл с именем  `.env`
6. Помещаем в него:
    * Токен Telegram для бота `TELEGRAM_TOKEN='Ваш_телеграмм_токен'`
    * Токен Telegram для отправки сообщений о ошибках `TELEGRAM_LOGS_TOKEN='Телеграмм_токен_бота_сообщений_о_ошибках'`
    * Chat id Телеграм бота сообщений о ошибках `TG_CHAT_ID='Ваш_chat_id_бота_сообщений_о_ошибках'`
    * Путь к файлу баз данных `PATH_TO_DB='путь/до/файла/базы_данных`

   

## Запуск бота Телеграм ##
`python bot.py`

## Пример работы Телеграм бота ##
Работающего телеграм бота можно посмотреть [тут](https://t.me/devman_sup_bot)

![rec_work_bot](https://github.com/IPRepin/love_bot/assets/76727704/16f4e365-59b5-4611-a0d3-2864923bd723)
