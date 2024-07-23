from telethon.sync import TelegramClient, events
from decouple import config
import logging
import requests
import json
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG)

bot_token = config('TELEGRAM_BOT_TOKEN')



# Telegram API base URL
API_BASE_URL = f'https://api.telegram.org/bot{bot_token}'

# Function to fetch updates from Telegram
def get_updates(offset=None, timeout=30):
    url = f"{API_BASE_URL}/getUpdates"
    params = {
        'offset': offset,
        'timeout': timeout
    }
    try:
        response = requests.get(url+'?timeout=10')
        #response.raise_for_status()  # Raise error for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching updates: {e}")
        return None

# Function to process incoming updates
def process_updates(updates):
    if not updates.get('ok', False):
        print(f"Failed to fetch updates: {updates.get('description', 'No description')}")
        return

    results = updates.get('result', [])
    for update in results:
        message = update.get('message') or update.get('edited_message')
        if message:
            message_text = message.get('text', 'No text')
            message_date = message.get('date', None)
            chat_id = message.get('chat', {}).get('id', 'Unknown')
            print(f"New message in chat ID {chat_id}:")
            print(f"Message: {message_text}")
            if message_date:
                print(f"Received at: {time.ctime(message_date)}")
            print('--' * 30)

# Main function to continuously fetch and process updates
def main():
    offset = None  # Initial offset, start from the beginning
    while True:
        updates = get_updates(offset)
        if updates:
            print(updates)
            print('-'*30)
            #process_updates(updates)
            # Update offset to fetch only new updates in the next iteration
            if updates['result']:
                offset = updates['result'][-1]['update_id'] + 1
        time.sleep(1)  # Polling interval

if __name__ == "__main__":
    print("Starting Telegram bot...")
    main()

