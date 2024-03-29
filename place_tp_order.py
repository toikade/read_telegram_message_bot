from decouple import config
from binance.client import Client


# Binance API key and secret
api_key = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
api_secret = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)

# Initialize the Binance Futures client
client = Client(api_key, api_secret, testnet=True)  # testnet=True for the Binance futures demo
