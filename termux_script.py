import logging
from telethon import TelegramClient, events
from decouple import config
import asyncio

# Set up logging to see detailed output
logging.basicConfig(level=logging.DEBUG)

# Initialize Telegram client
api_id = config('TELEGRAM_API_ID')
api_hash = config('TELEGRAM_API_HASH')
bot_token = config('TELEGRAM_BOT_TOKEN')

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
                'https://t.me/Gilanns',
                'https://t.me/crypto_hd']



async def main():
    async with TelegramClient('test', api_id, api_hash) as client:
        # Get channel entities for error handling
        chat_entities = []
        for url in channel_urls:
            try:
                chat_entity = await client.get_input_entity(url)
                chat_entities.append(chat_entity)
            except ValueError:
                print(f"Error getting entity for channel: {url}")

        # Define event handlers for each channel entity
        for chat_entity in chat_entities:
            @client.on(events.NewMessage(chats=chat_entity))
            async def handle_new_message(event):
                message_text = event.message.text
                channel_title = event.chat.title  # Access channel title from the event object
                channel_id = event.message.peer_id.channel_id

                print(f"{'-'*30}")
                print(f"{channel_id}|** Channel: {channel_title} **")
                print(f"Message: {message_text}\n")
                print(f"{'-'*30}")

        # Start the client (authentication might be required)
        print('Starting Telegram client...')
        await client.start()
        print('Listening for new messages...')

        # Run the client until disconnected
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
