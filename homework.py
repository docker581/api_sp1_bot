import os
import time
import requests
import telegram

import logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s:%(message)s',
)

from dotenv import load_dotenv
load_dotenv()

PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    if homework_name == None:
        print("Не удалось найти ключ homework['homework_name']")
    if homework['status'] == None:
        print("Не удалось найти ключ homework['status']")   
    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = ('Ревьюеру всё понравилось, '
        'можно приступать к следующему уроку.')
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    from_date = (int(time.time()) if current_timestamp is None 
        else current_timestamp)        
    params={'from_date':from_date}
    try:
        homework_statuses = requests.get(
            'https://praktikum.yandex.ru/api/user_api/homework_statuses/', 
            headers=headers,
            params=params,
        )
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise SystemExit(err)
    return homework_statuses.json()        


def send_message(message, bot_client):
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def main():
    bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time()) 
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(new_homework.get('homeworks')[0]),
                    bot_client,
                ),
            current_timestamp = new_homework.get(
                'current_date', 
                current_timestamp,
            )  
            time.sleep(1200)  

        except Exception as e:
            print(f'Бот столкнулся с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
