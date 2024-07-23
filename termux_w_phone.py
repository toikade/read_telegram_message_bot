import logging
from telethon import TelegramClient, events
from decouple import config

# Set up logging to see detailed output
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Telegram client
api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')

# List of channel URLs to monitor
channel_urls =['https://t.me/RynHumbleTrader',
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

async def main():
    async with TelegramClient('bot', api_id, api_hash) as client:
        chat_entities = []
        for url in channel_urls:
            try:
                entity = await client.get_entity(url)
                chat_entities.append(entity)
                logging.info(f'Added chat entity: {entity}')
            except Exception as e:
                logging.error(f'Error getting entity for {url}: {e}')

        logging.debug(f'Chat entities: {chat_entities}')

        @client.on(events.NewMessage(chats=chat_entities))
        async def handle_new_message(event):
            logging.info(f'New message event received: {event}')
            try:
                raw_message = event.message.text
                channel_id = event.message.peer_id.channel_id
                logging.info(f'New message from {channel_id} at {event.message.date}: {raw_message}')
                logging.info('--' * 30)
            except Exception as e:
                logging.error(f'Error handling message: {e}')

        logging.info('Listening for new messages...')
        await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
