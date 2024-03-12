from decouple import config
from binance.client import Client

# Initialize Binance client
api_key = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
api_secret = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)
client = Client(api_key, api_secret, testnet=True)

def get_symbol_market_value_and_divide_by_two(symbol):
    # Get the market value of the asset
    ticker = client.get_symbol_ticker(symbol=symbol)
    market_value = ticker['price']
    #convert the string to a float and divide it by 2
    divideBytwoPrice = float(market_value)/2
    return divideBytwoPrice




divided_value = get_symbol_market_value_and_divide_by_two('1INCHUSDT')
#print(f"Market value of {symbol}: {float(market_value)}")
print(divided_value)
