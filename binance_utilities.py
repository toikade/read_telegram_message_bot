import requests


# Base URL for Binance Futures API
BASE_URL = 'https://testnet.binancefuture.com'


# Function to get the current price of a symbol
def get_current_price(symbol):
    endpoint = '/fapi/v1/ticker/price'
    url = BASE_URL + endpoint
    response = requests.get(url, params={'symbol': symbol})
    data = response.json()
    return float(data['price'])

# Function to get symbol precision and filters
def get_symbol_info(symbol):
    endpoint = '/fapi/v1/exchangeInfo'
    url = BASE_URL + endpoint
    response = requests.get(url)
    data = response.json()
    for s in data['symbols']:
        if s['symbol'] == symbol:
            return s
    return None

# Function to get the current price of a symbol
def get_current_price(symbol):
    endpoint = '/fapi/v1/ticker/price'
    url = BASE_URL + endpoint
    response = requests.get(url, params={'symbol': symbol})
    data = response.json()
    return float(data['price'])


symbol = ['JASMYUSDT', '1INCHUSDT', 'BTCUSDT', 'YFIUSDT', 'SOLUSDT', 'ETHUSDT']
# for symbol in symbol:
#     print(get_symbol_info(symbol))
#     print(get_current_price(symbol))
#     print('='*30)