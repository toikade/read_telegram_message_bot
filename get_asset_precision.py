from binance.client import Client
from decouple import config

# Replace with your Binance API key and secret
api_key = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
api_secret = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)

# Initialize the Binance client
client = Client(api_key, api_secret, testnet=True)

def get_asset_precision(symbol):
    try:
        # Get exchange information
        exchange_info = client.futures_exchange_info()

        # Find the symbol details
        for symbol_info in exchange_info['symbols']:
            if symbol_info['symbol'] == symbol:
                return symbol_info['filters'][0]['tickSize']

        print(f"Symbol {symbol} not found.")
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    symbol = '1000PEPEUSDT'

    precision = get_asset_precision(symbol)
    if precision is not None:
        print(f"Precision for symbol {symbol}: {precision}")
    else:
        print('Nothing')
