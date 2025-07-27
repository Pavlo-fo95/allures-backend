
FROM python:3.10-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка рабочего каталога
WORKDIR /app

# Копирование зависимостей и установка Python-зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копирование всех файлов проекта
COPY . .

# Установка переменной PYTHONPATH (чтобы работали импорты из /services и /common)
ENV PYTHONPATH=/app:/app/common

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
