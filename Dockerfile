# Указываем базовый образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере, по умолчанию /app
WORKDIR /tf4
RUN pip install poetry
# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY requirements.txt ./
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости Python
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Копируем исходный код приложения в контейнер
COPY . .
