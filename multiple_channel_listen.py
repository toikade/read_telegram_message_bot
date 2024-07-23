from telethon.sync import TelegramClient, events
#from data_extract_functions import extract_signal_data_from_ai_crypto as extract_from_ai_crypto
#from data_extract_functions import extract_signal_data_from_sentinel as extract_from_sentinel
from data_extract_functions import extract_signal_data_from_harrisons
from decouple import config
import pytz
from datetime import datetime


# Initialize Telegram client
api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')
# List of channel URLs to monitor
channel_urls = ['https://t.me/crypto_headlines',
                'https://t.me/Mikegoldmasterofficia',
                'https://t.me/AiCryptoSignalsApp',
                't.me/SentinelCrypto',
                'https://t.me/RynHumbleTrader',
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
                'https://t.me/Harrison_Futures1',
                'https://t.me/Gilanns',
                'https://t.me/realcorrectscore_fixedmatches',
                'https://t.me/KingFuryPronos',
                'https://t.me/oracle_easy' ]

#COnvert Server time to my timezone
local_tz = pytz.timezone('Africa/Lagos')

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
            chat = await event.get_chat()
            chat_title = chat.title
            chat_username = chat.username
            sender = await client.get_entity(channel_id)
            message_time_utc = event.message.date
            message_time_local = message_time_utc.astimezone(local_tz)
            print(f"{channel_id}|{chat_title}|{chat_username}|{message_time_local}\n")
            print(raw_message)
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
                print('*='*15)
                print(raw_message)
            elif channel_id == 1461729353:    #oracle_easy
                print(raw_message)
            elif channel_id == 2042531820:    #unpaid ai_crypto
                #extract_from_ai_crypto(raw_message)
                print(raw_message)
                #print(tradeData)
            elif channel_id == 2058068801:      #harrisons1-free-scam
                print('*='*15)
                #print(raw_message)
                json_data_for_market = extract_signal_data_from_harrisons(raw_message)
                print(json_data_for_market)
            elif channel_id == 2041075234: #Harrisons_Futures1-free
                print('*='*15)
                #print(raw_message)
                json_data_for_market = extract_signal_data_from_harrisons(raw_message)
                print(json_data_for_market)
            else:
                pass
            print('--' * 30)

    # Run the client until disconnected
    print('Listening for new messages...')
    client.run_until_disconnected()
