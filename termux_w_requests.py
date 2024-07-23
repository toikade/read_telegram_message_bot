import asyncio
import logging
from telethon import TelegramClient, events
from decouple import config
import requests, time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace with your Telegram bot token
api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')

# List of channel URLs (replace with your actual channel URLs)
channel_urls = ['https://t.me/RynHumbleTrader',
                'https://t.me/Smc_indepth',
                'https://t.me/professorgold',
                'https://t.me/NetProfitFX',
                'https://t.me/Forexminds_signals',
                'https://t.me/usoilwtisignals',
                'https://t.me/usoil_crudoilsignal',
                'https://t.me/fxadvance1', 
                'https://t.me/GoldScalpingTrader1',
                'https://t.me/goldsnipers11',
                'https://t.me/EasyForexPips',
                'https://t.me/Real_Time_Forex_Signals',
                'https://t.me/Usoil_Crudeoil_Signal',
                'https://t.me/tradegold_pk',
                'https://t.me/Myc_forexsignals',
                'https://t.me/bengoldtrader',
                'https://t.me/Xaussdgoldmaster786',
                'https://t.me/OfficialJoshuaPipster',
                'https://t.me/crystalforex1',
                'https://t.me/ForexArtiumEA',
                'https://t.me/SuccessForexSignals',
                'https://t.me/Starnet_AIBang',
                'https://t.me/hugoswaytrade',
                'https://t.me/GoldzillaOfficial',
                'https://t.me/HarrisonFutures1',
                'https://t.me/Gilanns',
                'https://t.me/crypto_hd']


# Telegram API URL
api_url = f'https://api.telegram.org/bot{bot_token}'

# Function to extract username from URL
def extract_username_from_url(url):
    return url.split('/')[-1]

# Function to get chat ID of a channel
def get_chat_id(channel_username):
    url = f'{api_url}/getChat'
    try:
        response = requests.get(url, params={'chat_id': f'@{channel_username}'}, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data['ok']:
            return data['result']['id']
        else:
            logging.error(f"Failed to get chat ID for {channel_username}: {data['description']}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting chat ID for {channel_username}: {e}")
        return None

# Function to get updates from Telegram
def get_updates(offset=None):
    url = f'{api_url}/getUpdates'
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting updates: {e}")
        return {'ok': False, 'result': []}

# Get chat IDs for all channels
channel_ids = [get_chat_id(extract_username_from_url(url)) for url in channel_urls]

# Log the chat IDs
logging.debug(f"Channel IDs: {channel_ids}")

# Poll for new messages
def poll_for_messages():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        logging.debug(f"Updates: {updates}")
        if updates['ok']:
            for update in updates['result']:
                last_update_id = update['update_id'] + 1
                message = update.get('message') or update.get('channel_post')
                if message:
                    chat_id = message['chat']['id']
                    if chat_id in channel_ids:
                        channel_title = message['chat']['title']
                        message_text = message.get('text', 'No text')
                        message_date = message['date']
                        print(f"** Channel: {channel_title} **")
                        print(f"Message: {message_text}")
                        print(f"Date: {message_date}\n")
        time.sleep(1)

if __name__ == '__main__':
    poll_for_messages()