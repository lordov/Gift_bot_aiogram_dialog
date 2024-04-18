# Сборочный образ
FROM python:3.11-slim-bullseye as compile-image

# Создаем виртуальное окружение и устанавливаем зависимости
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Образ для запуска
FROM python:3.11-slim-bullseye as run-image

# Копируем виртуальное окружение из сборочного образа
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

# Копируем файлы бота в контейнер
COPY tgbot /app/tgbot

# Команда запуска бота
CMD ["python", "-m", "tgbot"]