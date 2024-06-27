# Используем базовый образ Python
FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /running

# Устанавливаем зависимости через pip
COPY ./requirements.txt /running/
RUN pip install -r /running/requirements.txt

# Копируем файлы проекта в контейнер
COPY . .
RUN rm -f .env