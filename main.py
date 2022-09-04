import requests
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    load_dotenv()
    devman_token = os.environ['DEVMAN_TOKEN']
    url = 'https://dvmn.org/api/user_reviews/'
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(response.json())
