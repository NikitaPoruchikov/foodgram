# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .


# Команда для запуска сервера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi:application"]

