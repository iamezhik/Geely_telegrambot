# Используем официальный образ Python
FROM python:3.10-slim

# Рабочая директория
WORKDIR /checker_bot

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё
COPY . .

# Запускаем бота
CMD ["python", "checker_bot.py"]
