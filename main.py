import requests
from dotenv import load_dotenv
import os
from time import sleep
import telegram


def prepare_message(attempt):
    lesson_title = attempt['lesson_title']
    if attempt['is_negative']:
        attempt_result = 'К сожалению, в работе нашлись ошибки.'
    else:
        attempt_result = 'Преподавателю все понравилось, можно приступать к следующему уроку.'
    lesson_url =  attempt['lesson_url']
    message = f'У вас проверили работу "{lesson_title}".\n{attempt_result} {lesson_url}'
    return message 


if __name__ == '__main__':

    load_dotenv()
    devman_token = os.environ['DEVMAN_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    bot = telegram.Bot(token=telegram_token)

    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    new_checks = response.json()

    if new_checks['status'] == 'timeout':
        timestamp = new_checks['timestamp_to_request']
    else:
        new_attempts = new_checks['new_attempts']
        for attempt in new_attempts:
            message = prepare_message(attempt)
            bot.send_message(chat_id=telegram_chat_id, text=message)
        timestamp = new_checks['last_attempt_timestamp']

    while True:

        try:
            params = {'timestamp': timestamp}
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            new_checks = response.json()
            new_attempts = new_checks['new_attempts']
            for attempt in new_attempts:
                message = prepare_message(attempt)
                bot.send_message(chat_id=telegram_chat_id, text=message)

            timestamp = new_checks['last_attempt_timestamp']

        except requests.exceptions.ReadTimeout:
            print('Обновлений нет')

        except requests.exceptions.ConnectionError:
            print('Потеряно интернет соединение...')
            sleep(10)
