FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /my-docker

# Устанавливаем системные библиотеки
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы в контейнер
COPY . /my-docker

# Устанавливаем зависимости из requirements.txt
RUN pip install -r requirements.txt

# Указываем порт для приложения
EXPOSE 8000

# Запускаем приложение
CMD ["python", "app.py"]
