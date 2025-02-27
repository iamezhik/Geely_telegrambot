# Telegram Bot для проверки технических акций Geely Russia по VIN номеру автомобиля

Автоматизированный бот для проверки наличия технических акций для вашего автомобиля на официальном сайте Geely. Отправляет уведомления в Telegram при изменении информации о технических акциях.

## Содержание
1. [Требования](#требования)
2. [Установка Docker](#установка-docker)
3. [Настройка бота](#настройка-бота)
4. [Запуск в Docker](#запуск-в-docker)
5. [Ручная установка (без Docker)](#ручная-установка-без-docker)
6. [Использование](#использование)
7. [Изменение данных пользователя или обновление](#обновление)
8. [Устранение неполадок](#устранение-неполадок)
9. [Важные примечания](#важные-примечания)

---

## Требования
- Операционная система: Ubuntu 22.04 LTS или новее для установки по гайду ниже
  
---

## Установка Docker (если выхотите запускать бота в контейнере)

1. Обновите систему при необходимости
```bash
sudo apt update && sudo apt upgrade -y
```
2. Установите необходимые пакеты:
```bash
sudo apt install nano git -y
```
3. Установите Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```
---

## Настройка бота

1. Скачайте репозиторий:
```bash
git clone https://github.com/iamezhik/Geely_telegrambot.git
cd geely_telegrambot
```
2. Отредактируйте содержимое файла с переменными (вставьте свои значения):
```bash
nano .env
```
---

## Запуск в Docker

1. Соберите контейнер:
```bash
docker-compose build
```
2. Запустите бота:
```bash
docker-compose up -d
```
3. Проверьте статус:
```bash
docker-compose ps
```
4. Если вы все сделали правильно, то вам в чат с ботом придет первое сообщение.
---

## Ручная установка (без Docker)

1. Установите Python:
```bash
sudo apt install python3.10 python3.10-venv -y
```
2. Создайте виртуальное окружение python для изоляции библиотек:
```bash
python3.10 -m venv venv
source venv/bin/activate
```
3. Установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```
4. Запустите бота:
```bash
python3 checker_bot.py
```
---

## Использование

1. В Telegram найдите вашего бота по имени
2. Отправьте команды:
   - `/start` — показать справку
   - `/check` — выполнить ручную проверку

---

## Изменение данных пользователя или обновление

1. Остановите контейнер или убейте процесс, если запускали без Docker:
```bash
docker-compose down
```
```bash
pkill -f checker_bot.py
```
2. Измените переменные в .env, если вы их указали неверно, либо с помощью git pull скачайте новую версию бота (которой не будет, ибо незачем 😑)
3. Пересоберите контейнер или запустите заново с python:
```bash
docker-compose up -d --build
```
```bash
python3 checker_bot.py
```
## Устранение неполадок

1. Просмотр логов:
```bash
docker-compose logs -f
```
2. Проверка работы бота (запуск ручками):
```bash
docker exec -it checker-bot python3 checker_bot.py --test
```
3. Проверка сетевого соединения:
```bash
curl -I https://www.geely-motors.com
```

---

## Важные примечания

1. **Про ботов в Telegram**:
   - [Как создать бота и узнать его токен](https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a#create-a-telegram-bot-and-get-a-bot-token)
   - [Как узнать CHAT_ID приватного чата с ботом](https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a#get-chat-id-for-a-private-chat)
   - CHAT_ID нужен, для того чтобы бот мог писать вам сообщения при автоматической проверке. Если его не указать, то теоретически бот будет работать, но только по команде **/check**
2. **Расписание проверок**:
   - По умолчанию проверка выполняется каждые 24 часа
   - Для изменения интервала отредактируйте `CHECK_INTERVAL` в `.env`
   - Бот не будет присылать уведомления, если статус не изменился! Бессмысленно читать каждый день, что "Доступных акций нет".
   - Если очень надо проверить все ли работает, запустите запрос ручками: **/check**
3. **Логирование**:
   - Все события сохраняются в системный журнал Docker
   - Для экспорта логов:
   ```bash
   docker-compose logs > bot.log
   ```
   - При запуске без Docker логи выводятся в консоль
