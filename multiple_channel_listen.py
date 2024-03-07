from telethon.sync import TelegramClient, events
from data_extract_functions import extract_signal_data_from_ai_crypto as extract_from_ai_crypto

# Initialize Telegram client
api_id = '21243794'
api_hash = '2a1ef85eff1fe10eb27560df055b1746'
bot_token = '6379620803:AAEaLOHQM6Zeo3niZFDDDjS4NnkH1S2NqqM'  # 'your_bot_token'

# List of channel URLs to monitor
channel_urls = ['https://t.me/+6Lg31Rwf1UtlYWFk', 't.me/+6Lg31Rwf1UtlYWFk', 't.me/SentinelCrypto', 'https://t.me/Gilanns', 'https://t.me/crypto_headlines']

with TelegramClient('test', api_id, api_hash) as client:
    # Get the input entity for each channel
    chat_entities = [client.get_input_entity(url) for url in channel_urls]
    #print(chat_entities)

    # Define event handlers for each channel
    for chat_entity in chat_entities:
        @client.on(events.NewMessage(chats=chat_entity))
        async def handle_new_message(event):
            raw_message = event.message.text
            channel_id = event.message.peer_id.channel_id
            print(channel_id)
            #print(event)
            print(f'New message from {event.message.date}: {raw_message}')
            tradeData = {}
            if channel_id == '2074626472':
                extract_from_ai_crypto(raw_message)
                print(tradeData)
            print('--' * 30)

    # Run the client until disconnected
    print('Listening for new messages...')
    client.run_until_disconnected()
