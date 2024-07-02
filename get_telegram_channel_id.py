from decouple import config
from telethon import TelegramClient
import asyncio

# Load the credentials from the .env file
api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')

# Function to get the channel ID
async def get_channel_id(channel_username):
    client = TelegramClient('bot', api_id, api_hash)

    await client.start(bot_token=bot_token)
    try:
        # Get the channel entity
        channel = await client.get_entity(channel_username)
        print(f'Channel ID: {channel.id}')
    finally:
        await client.disconnect()

# Example usage
channel_username = 'https://t.me/HarrisonFutures1'

asyncio.run(get_channel_id(channel_username))
