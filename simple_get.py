from telethon.sync import TelegramClient, events
from datetime import datetime
from data_extract_functions import extract_signal_data_from_harrisons
import time
import pytz
from decouple import config

# Initialize Telegram client
api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')


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
    last_stored_id = 0
    
    with TelegramClient('test', api_id, api_hash) as client:
        chat_entity = client.get_input_entity('https://t.me/Harrison_Futures1')
        chat = client.get_entity(chat_entity)
        chat_title = chat.title
        chat_id = chat.id
        
        while True:
            messages = get_messages(client, chat_entity)
            for msg in messages:
                if not msg.text:
                    print(msg)
                    continue          
                local_date = msg.date.astimezone(lagos_tz)
                print(f"[{local_date}] | {chat_title} | msgID:{msg.id} | chatID:{chat_id}\n{msg.text}")
                print('-'*40)
                print(f"msgID:{msg.id} | last_stored:{last_stored_id}")
                #if the ID of the message>than the id of the last relevant message stored(so as to avoid parsing
                # the same message on each poll)
                if msg.id > last_stored_id:
                    #if criteria met parse the message to extract important data
                    json_data_for_market = extract_signal_data_from_harrisons(msg.text)
                    #if None is not returned i.e parsing was succesful
                    if json_data_for_market:
                        #last_stored_id is updated with the id of the most recent relevant message, so that
                        #next time the message id must be > this to be considered
                        last_stored_id = msg.id
                print(json_data_for_market)
                print('='*40)

            
            print('+=|'*35)
            now = datetime.now(lagos_tz)
            print(f"{now}")
            time.sleep(60)  # wait for 1 minute

if __name__ == '__main__':
    main()