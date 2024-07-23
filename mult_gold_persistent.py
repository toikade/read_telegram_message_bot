import tracemalloc
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, RPCError
from decouple import config
import asyncio

# Start tracing memory allocations
tracemalloc.start()

# Initialize Telegram client
api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')  # 'your_bot_token'

# List of channel URLs to monitor
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
                'https://t.me/Gilanns']

client = TelegramClient('bot', api_id, api_hash)

async def main():
    while True:
        try:
            await client.start(bot_token=bot_token)
            # Get the input entity for each channel
            chat_entities = []
            for url in channel_urls:
                try:
                    entity = await client.get_entity(url)
                    chat_entities.append(entity)
                except Exception as e:
                    print(f'Error getting entity for {url}: {e}')

            # Debugging: Print chat entities
            print(f'Chat entities: {chat_entities}')

            # Define event handlers for each channel
            @client.on(events.NewMessage(chats=chat_entities))
            async def handle_new_message(event):
                try:
                    raw_message = event.message.text
                    channel_id = event.message.peer_id.channel_id
                    print(f'New message from {channel_id} at {event.message.date}: {raw_message}')
                    print('--' * 30)
                except Exception as e:
                    print(f'Error handling message: {e}')

            # Notify that the bot is listening for messages
            print('Listening for new messages...')

            # Run the client until disconnected
            await client.run_until_disconnected()

        except FloodWaitError as e:
            print(f'FloodWaitError: Need to wait for {e.seconds} seconds')
            await asyncio.sleep(e.seconds)
        except RPCError as e:
            print(f'RPCError: {e}. Retrying in 5 seconds...')
            await asyncio.sleep(5)
        except Exception as e:
            print(f'Unexpected error: {e}. Retrying in 5 seconds...')
            await asyncio.sleep(5)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
