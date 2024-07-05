import telethon
from telethon.sync import TelegramClient, events
from decouple import config

api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')

# Define a list of channels you want to monitor
channel_urls = [
    'https://t.me/HarrisonFutures1',
    'https://t.me/oracle_easy',
    't.me/SentinelCrypto',
    'https://t.me/Gilanns'
]

with TelegramClient('test', api_id, api_hash) as client:

    # Create a list to hold all chat entities for channels
    chat_entities = []

    # Get the input entity for each channel
    for url in channel_urls:
        chat_entity = client.get_input_entity(url)
        chat_entities.append(chat_entity)

        # Define the event handler for new messages for each channel
        @client.on(events.NewMessage(chats=chat_entity))
        async def handle_new_message(event):
            print(f'New message from {event.message.date}: {event.message.text}')
            print('--' * 30)

    # Run the client until disconnected
    client.run_until_disconnected()
