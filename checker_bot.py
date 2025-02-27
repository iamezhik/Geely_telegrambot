import os
import logging
import telebot
import requests
from bs4 import BeautifulSoup
from threading import Timer
from dotenv import load_dotenv

# Настройка окружения и логгера
load_dotenv()
logging.basicConfig(level=logging.INFO)

class VinChecker:
    def __init__(self):
        self.bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
        self.vin = os.getenv('VIN_NUMBER')
        self.chat_id = os.getenv('CHAT_ID')
        self.last_result = None
        self.check_interval = int(os.getenv('CHECK_INTERVAL', 86400))  # По умолчанию 24 часа
        
        # Регистрация обработчиков команд
        self.bot.message_handler(commands=['start', 'help'])(self.send_welcome)
        self.bot.message_handler(commands=['check'])(self.manual_check)
        
    def send_welcome(self, message):
        """Обработчик команд start/help"""
        self.bot.reply_to(message, "🔍 Бот для проверки технических акций Geely по VIN. Доступные команды:\n/check - ручная проверка")

    def start_periodic_check(self):
        """Запуск периодической проверки"""
        self.schedule_check()
        self.bot.polling(none_stop=True)

    def schedule_check(self):
        """Планировщик периодической проверки"""
        Timer(self.check_interval, self.schedule_check).start()
        self.automatic_check()

    def automatic_check(self):
        """Автоматическая проверка с обработкой результатов"""
        try:
            result = self.fetch_vin_data()
            if result and result != "Доступных акций нет" and result != self.last_result:
                self.last_result = result
                self.bot.send_message(self.chat_id, f"🔔 Обновление статуса:\n{result}")
                logging.info("Отправлено автоматическое уведомление")
        except Exception as e:
            logging.error(f"Ошибка автоматической проверки: {str(e)}")

    def manual_check(self, message):
        """Ручная проверка по команде /check"""
        try:
            result = self.fetch_vin_data()
            response = result if result else "⚠️ Не удалось получить данные"
            self.bot.reply_to(message, response)
        except Exception as e:
            self.bot.reply_to(message, f"❌ Ошибка: {str(e)}")
            logging.error(f"Ошибка ручной проверки: {str(e)}")

    def fetch_vin_data(self):
        """Основная логика получения данных по VIN"""
        with requests.Session() as session:
            try:
                # Первичный запрос для получения cookies
                session.get(
                    'https://www.geely-motors.com/for-owners/technical-center/technical-campaigns',
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                )

                # Отправка POST-запроса
                response = session.post(
                    'https://www.geely-motors.com/local/ajax/technicalcampaigns_redesign.php',
                    data={
                        'vin': self.vin,
                        'sessid': session.cookies.get('PHPSESSID', ''),
                        'ajaxAction': 'checkVin',
                        'componentName': 'geely:technical.campaigns'
                    },
                    headers={
                        'Bx-ajax': 'true',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Referer': 'https://www.geely-motors.com/for-owners/technical-center/technical-campaigns'
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        soup = BeautifulSoup(data.get('html', ''), 'html.parser')
                        result = soup.find('p', class_='technical-campaigns__vin-search-table-text')
                        return result.text if result else "Доступных акций нет"
                    return data.get('data', 'Ошибка при обработке запроса')
                return "Сервер не ответил корректно"

            except requests.RequestException as e:
                logging.error(f"Ошибка сети: {str(e)}")
                return None

if __name__ == '__main__':
    checker = VinChecker()
    checker.start_periodic_check()
