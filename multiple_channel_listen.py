from telethon.sync import TelegramClient, events
#from data_extract_functions import extract_signal_data_from_ai_crypto as extract_from_ai_crypto
#from data_extract_functions import extract_signal_data_from_sentinel as extract_from_sentinel
from data_extract_functions import extract_signal_data_from_harrisons
from decouple import config

# Initialize Telegram client
api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')
# List of channel URLs to monitor
channel_urls = ['https://t.me/crypto_headlines','https://t.me/AiCryptoSignalsApp','https://t.me/oracle_easy','t.me/SentinelCrypto','https://t.me/Gilanns' ]

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
            #print(f'New message from {event.message.date}: {raw_message}')
            tradeData = {}
            # if channel_id == 2074626472:    #ai_crypto_channel_vip
            #     extract_from_ai_crypto(raw_message)
            #     print(raw_message)
            #     print(tradeData)
            if channel_id == 1953834653:    #sentinel_crypto_channel
                #extract_from_sentinel(raw_message)
                print(raw_message)
            elif channel_id == 1598733237:    #gillans_crypto
                print(raw_message)
            elif channel_id == 1461729353:    #oracle_easy
                print(raw_message)
            elif channel_id == 2042531820:    #unpaid ai_crypto
                #extract_from_ai_crypto(raw_message)
                print(raw_message)
                #print(tradeData)
            elif channel_id == 2058068801:      #harrisons1-free
                print(raw_message)
                json_data_for_market = extract_signal_data_from_harrisons(raw_message)
                print(json_data_for_market)
            else:
                pass
            print('--' * 30)

    # Run the client until disconnected
    print('Listening for new messages...')
    client.run_until_disconnected()
