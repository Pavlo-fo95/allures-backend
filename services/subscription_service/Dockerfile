FROM python:3.10-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        python3-dev \
        libpq-dev \
        unixodbc \
        unixodbc-dev \
        curl \
        gnupg2 \
        ca-certificates \
        apt-transport-https && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Настройка переменной окружения
ENV PYTHONPATH=/app:/app/common

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
