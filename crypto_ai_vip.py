import telethon
from telethon.sync import TelegramClient, events
import datetime
import re

api_id = '21243794'
api_hash = '2a1ef85eff1fe10eb27560df055b1746'
bot_token = '6379620803:AAEaLOHQM6Zeo3niZFDDDjS4NnkH1S2NqqM'  #'your_bot_token'


with TelegramClient('test', api_id, api_hash) as client:
    chat_entity = client.get_input_entity('https://t.me/AiCryptoSignalsApp')
    #get the messages for today
    for message in client.iter_messages(chat_entity, offset_date=datetime.date.today(), reverse=True):
        print(f'New message from {message.date}: {message.text}')
        #print(message.text)
        print('-'*30)