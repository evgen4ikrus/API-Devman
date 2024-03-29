# API-Devman
Скрипт предназначен для работы с сервисом [Devman](https://dvmn.org/), присылает уведомления в telegram при проверке вашей работы преподавателем.
## Установка
Для работы скрипта вам понадобится Python третьей версии.

Скачайте код с GitHub. Затем установите зависимости:

```sh
pip install -r requirements.txt
```
## Переменные окружения
Для работы со скриптом вам понадобятся: токен и id чата вашего телеграм бота, [токен](https://dvmn.org/api/docs/) с сайта [Devman](https://dvmn.org/).
* Создайте файд .env в папке проекта
* Добавьте в файл переменные окружения, пример:
```
DEVMAN_TOKEN=834d51br0116fb17c53afa3d950eaea4551066c1
TELEGRAM_TOKEN=5516583653:AAERHDDNaolh-zc7tVr-UYTgMrg24BT8hPo
TELEGRAM_CHAT_ID=@ivanovivan  # для логов
TG_CHAT_ID=1774521104  # для оповещений
```
## Запуск и работа
Запустите скрипт командой:
```
python main.py
```
Если вы отправите работу на проверку с сайта [Devman](https://dvmn.org/) и преподаватель ее проверит, вам придет уведомление об этом в telegram.

Чтобы проверить работу скрипта, отправьте работу на проверку и тут же верните ее с проверки, должно прийти уведомление о проверенной работе.

## Запуск с помощью Docker
Проект подготовлен для запуска в Docker. Docker должен быть установлен ([Туториал по Docker](https://docs.docker.com/get-started/overview/)).

Для создания образа введите команду:
```
 docker build -t <имя образа> . 
```
Запуск:
```
docker run -dp 3000:3000 <имя образа>
```
Бот запущен.
