import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from decouple import config

# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot_token = config('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Command handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot.')

# Message handler for any text message
def handle_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    chat_title = update.message.chat.title if update.message.chat.title else 'Private Chat'
    user_name = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    message_text = update.message.text

    print(f"New message in group '{chat_title}' from user '{user_name}': {message_text}")

def main():
    # Initialize the Updater and Dispatcher
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM, or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
