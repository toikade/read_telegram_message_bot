import telethon
from telethon.sync import TelegramClient, events
import datetime
from decouple import config

api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')

with TelegramClient('test', api_id, api_hash) as client:

    # Get the input entity for the channel
    chat_entity = client.get_input_entity('https://t.me/HarrisonFutures1')

    # Define the event handler for new messages
    @client.on(events.NewMessage(chats=chat_entity))
    async def handle_new_message(event):
        print(f'New message from {event.message.date}:\n {event.message.text}')
        print('--' * 30)

    # Run the client until disconnected
    client.run_until_disconnected()
