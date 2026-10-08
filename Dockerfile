
FROM python:3.12-slim

# Установить рабочую директорию внутри контейнера
WORKDIR /app

# Установить системные зависимости, необходимые для psycopg2 (работы с PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Запретить Python писать файлы кэша .pyc на диск
ENV PYTHONDONTWRITEBYTECODE=1
# Запретить Python буферизовать потоки ввода-вывода (для красивых логов в докере)
ENV PYTHONUNBUFFERED=1

# Скопировать файл зависимостей и установить их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать весь код нашего проекта в контейнер
COPY . /app/
