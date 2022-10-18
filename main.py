import logging
import os
import time
from time import sleep

import requests
import telegram
from dotenv import load_dotenv


logger = logging.getLogger('Loger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def prepare_message(attempt):
    lesson_title = attempt['lesson_title']
    if attempt['is_negative']:
        attempt_result = 'К сожалению, в работе нашлись ошибки.'
    else:
        attempt_result = 'Преподавателю все понравилось, можно приступать к следующему уроку.'
    lesson_url = attempt['lesson_url']
    message = f'У вас проверили работу "{lesson_title}".\n\n{attempt_result}\n{lesson_url}'
    return message


def main():
    logging.basicConfig(level=logging.INFO)

    load_dotenv()
    devman_token = os.environ['DEVMAN_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    tg_chat_id = os.environ['TG_CHAT_ID']
    bot = telegram.Bot(token=telegram_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, telegram_chat_id))
    logger.info('Бот запущен')

    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_token}'
    }

    timestamp = time.time()
    timeout = 90

    while True:

        try:
            params = {'timestamp': timestamp}
            response = requests.get(url, headers=headers,
                                    params=params, timeout=timeout)
            response.raise_for_status()

            review_response = response.json()
            if review_response['status'] == 'timeout':
                timestamp = review_response['timestamp_to_request']
            else:
                new_attempts = review_response['new_attempts']
                for attempt in new_attempts:
                    message = prepare_message(attempt)
                    bot.send_message(chat_id=tg_chat_id, text=message)
                timestamp = review_response['last_attempt_timestamp']

        except requests.exceptions.ReadTimeout:
            logger.warning('Нет ответа от сервера')

        except requests.exceptions.ConnectionError:
            logger.warning('Потеряно интернет соединение')
            sleep(10)

        except Exception:
            logger.exception('Произошла ошибка:')


if __name__ == '__main__':
    main()
