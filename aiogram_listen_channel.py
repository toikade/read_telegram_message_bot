import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ChatType
from decouple import config

# Load your API Token from environment variables or directly input here
bot_token = config('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# List of channel usernames or IDs you want to listen to
# Use the @username format or channel ID
CHANNELS = ['@HarrisonFutures1', '@Gilanns','https://t.me/HarrisonFutures1']

@dp.message_handler(chat_type=[ChatType.CHANNEL])
async def handle_channel_message(message: types.Message):
    if message.chat.username in CHANNELS:
        logging.info(f"Received message in {message.chat.title}: {message.text}")
        await message.reply(f"Received your message: {message.text}")

async def on_startup(dp):
    logging.info('Bot is starting...')

async def on_shutdown(dp):
    logging.info('Bot is shutting down...')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
