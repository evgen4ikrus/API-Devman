import requests
from dotenv import load_dotenv
import os
from time import sleep
import telegram


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
        bot.send_message(chat_id=telegram_chat_id, text='Преподаватель проверил работу!')
        timestamp = new_checks['last_attempt_timestamp']

    while True:

        try:
            params = {
                'timestamp': timestamp
            }
            response = requests.get(url, headers=headers, params=params, timeout=5)
            response.raise_for_status()
            timestamp = response.json()['last_attempt_timestamp']
            bot.send_message(chat_id=telegram_chat_id, text='Преподаватель проверил работу!')

        except requests.exceptions.ReadTimeout:
            print('Обновлений нет')
        except requests.exceptions.ConnectionError:
            print('Потеряно интернет соединение...')
            sleep(10)
