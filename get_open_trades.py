from decouple import config
from binance.client import Client
import time


# Binance API key and secret
api_key = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
api_secret = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)

# Initialize the Binance Futures client
client = Client(api_key, api_secret, testnet=True)  # testnet=True for the Binance futures demo

# Query all open orders across all symbols (trading pairs)
open_trades = client.futures_get_open_orders()

# Print the details of each open trade
for trade in open_trades:
    print('Trade ID:', trade['orderId'])
    print('Symbol:', trade['symbol'])
    print('Side:', trade['side'])
    print('Quantity:', trade['origQty'])
    print('Price:', trade['price'])
    print('----------------------------------')
print(f'{len(open_trades)} open orders')