import os
import time
import requests

from twilio.rest import Client

from dotenv import load_dotenv
load_dotenv()

URL = 'https://api.vk.com/method/'
VK_VERSION = 5.92
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
# определяем здесь, т.к. по pytest sms_sender() вызывается с 1 параметром
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'v': VK_VERSION,
        'access_token': ACCESS_TOKEN,
        'fields': 'online',
    }
    status = requests.post(
        '{}users.get'.format(URL), 
        params=params,
    )
    try:
        status_online = status.json()['response'][0].get('online')
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    return status_online


def sms_sender(sms_text):
    message = CLIENT.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO,
    )
    return message.sid 


if __name__ == '__main__':
    vk_id = input('Введите id: ')
    while True:
        if get_status(vk_id) == 1:   
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
