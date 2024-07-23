import logging
from telethon import TelegramClient, events
from decouple import config

# Set up logging to see detailed output
logging.basicConfig(level=logging.DEBUG)

# Initialize Telegram client
api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')

client = TelegramClient('anon', api_id, api_hash)
try:
    @client.on(events.NewMessage)
    async def my_event_handler(event):
        # Good
        chat = await event.get_chat()
        sender = await event.get_sender()
        chat_id = event.chat_id
        sender_id = event.sender_id
        raw_message = event.message.text
        print([chat, sender, chat_id, sender_id, raw_message])
        logging.info(f'New message event received: {event}')
except Exception as e:
    logging.error(f"error handling: {e}")

client.start()
client.run_until_disconnected()