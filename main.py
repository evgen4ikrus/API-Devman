import requests
from dotenv import load_dotenv
import os
from time import sleep


if __name__ == '__main__':
    load_dotenv()
    devman_token = os.environ['DEVMAN_TOKEN']
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            print(response.json())
        except requests.exceptions.ReadTimeout:
            print('Обновлений нет')
        except requests.exceptions.ConnectionError:
            print('Потеряно интернет соединение...')
            sleep(10)
