# Pet-проект: Бот на AIogram-dialog для проведения небольших розыгрышей

Этот бот был разработан, в том числе, для тестирования и использования современных технологий, таких как Redis, Docker, Docker-compose, RabbitMQ (в будущем), и Fluent (в будущем).

## Обзор проекта

Этот репозиторий содержит Telegram бота, созданного с использованием фреймворка AIogram-dialog для проведения небольших розыгрышей. Здесь вы найдете объяснения и инструкции для тех, кто столкнется с этим проектом.

## Установка с помощью Docker и Docker-compose

### Создание Docker образа локально (или использование DockerHub для будущих действий)
1. `docker build -t name/mybot:version .`  
   Пример: `docker build -t lordovat/testrep:mybot_redis .`

### Альтернатива: Загрузка образа с DockerHub
1.1 `docker pull lordovat/testrep:mybot_latest`

### Запуск с Docker-compose
2. `docker-compose up --build`

## Запуск из репозитория

1. Клонируйте репозиторий.
2. Переместите файл `tgbot/__main__.py` в корень проекта, где расположены файлы `.env` и `Dockerfile`.
3. Запустите приложение после заполнения вашего файла `.env`  пример `.env` представлен в `.env.example`.

Примечание: Этот проект использует базу данных MySQL, поэтому убедитесь, что вы настроили свою базу данных перед запуском, будь то локально или удаленно.

Размещаю этот материал для новичков+ т.к материалов для русскоязычного коммьюнити не много. Тут не много информации, но что-нибудь может будет полезным.
Не стесняйтесь вносить свой вклад или использовать этот проект в качестве учебного ресурса для изучения!

```
Gift_bot_aiogram_dialog
├─ .dockerignore
├─ docker-compose.yml
├─ Dockerfile
├─ Logs
├─ nats_data
├─ README.md
├─ requirements.txt
└─ tgbot
   ├─ constants.py
   ├─ DB
   │  ├─ db.py
   │  └─ __init__.py
   ├─ dialogs
   │  ├─ admin_dialog
   │  │  ├─ admin_callback.py
   │  │  ├─ admin_panel.py
   │  │  └─ __init__.py
   │  ├─ getters.py
   │  ├─ Standart_dialog
   │  │  ├─ base_callback.py
   │  │  ├─ base_menu.py
   │  │  └─ __init__.py
   │  ├─ states.py
   │  └─ __init__.py
   ├─ handlers
   │  ├─ standart_handlers.py
   │  └─ __init__.py
   ├─ kbd
   │  ├─ keyboards.py
   │  └─ __init__.py
   ├─ utils
   │  ├─ commands.py
   │  ├─ config.py
   │  ├─ logger_config.py
   │  ├─ numbers.py
   │  └─ __init.py
   └─ __main__.py

```