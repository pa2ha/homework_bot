import logging
import os
import sys
import time
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверка доступности переменных окружения."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        chat_id = TELEGRAM_CHAT_ID
        bot.send_message(chat_id, message)
        logger.debug(f'Отправлено сообщение: {message}')
    except Exception:
        raise Exception(f'Не удалось отправить сообщение {message}.')


def get_api_answer(timestamp):
    """Делаем запрос к API сервесу.
    Возвращаем ответприведённый к типу даных Python.
    """
    try:
        timestamp = timestamp or int(time.time())
        payload = {'from_date': timestamp}
        homework_statuses = requests.get(ENDPOINT, headers=HEADERS,
                                         params=payload)
        status = homework_statuses.status_code
        if status != HTTPStatus.OK:
            raise AssertionError(
                f'Недоступность эндпоинта {ENDPOINT}. Код ответа API: {status}'
            )
        return homework_statuses.json()
    except requests.RequestException:
        raise AssertionError(
            'Убедитесь, что в функции `get_api_answer` обрабатывается '
            'ситуация, когда при запросе к API возникает исключение '
            '`requests.RequestException`.'
        )


def check_response(response):
    """Проверяет ответ API на соответствие ожидаемой структуре."""
    if not isinstance(response, dict):
        raise TypeError('Ответ API не является словарем.')
    homeworks = response.get('homeworks')
    cur_date = response.get('current_date')
    if (homeworks is None or cur_date is None):
        raise KeyError('Ошибка в получении значений словаря.')
    if not isinstance(homeworks, list):
        raise TypeError(f'Ответ API: {response}, не соответствует ожиданиям.')

    return homeworks


def parse_status(homework):
    """Извлекаем статус конкретно взятой работы и возвращаем вердикт."""
    homework_name = homework.get('homework_name')
    if not homework_name:
        raise KeyError(f'Отсутствует или пустое поле: {homework_name}')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_VERDICTS:
        raise KeyError(f'Неизвестный статус: {homework_status}')
    verdict = HOMEWORK_VERDICTS.get(homework_status)
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Отсутствует одна или несколько переменных окружения')
        sys.exit()
    bot = Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            if homeworks:
                message = parse_status(homeworks[0])
                send_message(bot, message)
            else:
                timestamp = response.get('current_date')
        except Exception as error:
            logger.error(error)
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
