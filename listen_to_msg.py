import telethon
from telethon.sync import TelegramClient, events
import datetime

api_id = '21243794'
api_hash = '2a1ef85eff1fe10eb27560df055b1746'
bot_token = '6379620803:AAEaLOHQM6Zeo3niZFDDDjS4NnkH1S2NqqM'  # 'your_bot_token'

with TelegramClient('test', api_id, api_hash) as client:

    # Get the input entity for the channel
    chat_entity = client.get_input_entity('https://t.me/+6Lg31Rwf1UtlYWFk')

    # Define the event handler for new messages
    @client.on(events.NewMessage(chats=chat_entity))
    async def handle_new_message(event):
        print(f'New message from {event.message.date}: {event.message.text}')
        print('--' * 30)

    # Run the client until disconnected
    print('Listening for new messages...')
    client.run_until_disconnected()
