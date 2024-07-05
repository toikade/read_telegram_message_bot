import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from decouple import config

# Load your bot token
bot_token = config('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# List of channel usernames you want to listen to
CHANNELS = ['@HarrisonFutures1', '@Gilanns', 'https://t.me/HarrisonFutures1']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Bot started!')

async def handle_channel_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.username in CHANNELS:
        logging.info(f"Received message in {update.message.chat.title}: {update.message.text}")
        await update.message.reply_text(f"Received your message: {update.message.text}")

def main():
    # Create the Application and pass it your bot token.
    application = Application.builder().token(bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non-command messages from channels - handle the message
    for channel in CHANNELS:
        application.add_handler(MessageHandler(filters.Chat(channel) & filters.TEXT, handle_channel_message))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
