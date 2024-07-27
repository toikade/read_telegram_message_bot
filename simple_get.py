from telethon.sync import TelegramClient, events
from datetime import datetime
from data_extract_functions import extract_signal_data_from_harrisons
import time
import pytz

api_id = '21243794'
api_hash = '2a1ef85eff1fe10eb27560df055b1746'
bot_token = '6379620803:AAEaLOHQM6Zeo3niZFDDDjS4NnkH1S2NqqM'  #'your_bot_token'


def get_messages(client, chat_entity):
    messages = []
    
    for message in client.iter_messages(chat_entity, limit=10):
        #messages.append(message.text)
        messages.append(message)

    # Sort messages by ID (oldest to most recent)
    messages.sort(key=lambda msg: msg.id)
    
    return messages

def main():
    lagos_tz = pytz.timezone('Africa/Lagos')
    
    with TelegramClient('test', api_id, api_hash) as client:
        chat_entity = client.get_input_entity('https://t.me/Harrison_Futures1')
        chat = client.get_entity(chat_entity)
        chat_title = chat.title
        chat_id = chat.id
        
        while True:
            messages = get_messages(client, chat_entity)
            for msg in messages:             
                local_date = msg.date.astimezone(lagos_tz)
                print(f"[{local_date}] | {chat_title} | {msg.id} | chatID:{chat_id}\n{msg.text}")
                print('-'*40)
                json_data_for_market = extract_signal_data_from_harrisons(msg.text)
                print(json_data_for_market)
                print('='*40)

            
            print('+=|'*35)
            now = datetime.now(lagos_tz)
            print(f"{now}")
            time.sleep(60)  # wait for 1 minute

if __name__ == '__main__':
    main()