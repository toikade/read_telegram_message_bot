import requests
import json
import hmac
import hashlib
import time
from decouple import config

# Binance API credentials
api_key = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
api_secret = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)

# Function to generate the signature
def create_signature(params, secret):
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


def get_positions(api_key, api_secret):
    params = {
        'timestamp': int(time.time() * 1000),
        'recvWindow': 5000
    }
    params['signature'] = create_signature(params, api_secret)
    headers = {'X-MBX-APIKEY': api_key}
    response = requests.get('https://fapi.binance.com/fapi/v1/position', headers=headers, params=params)
    return json.loads(response.text)

def get_account_info(api_key, api_secret):
    params = {
        'timestamp': int(time.time() * 1000),
        'recvWindow': 5000
    }
    params['signature'] = create_signature(params, api_secret)
    headers = {'X-MBX-APIKEY': api_key}
    response = requests.get('https://api.binance.com/api/v3/account', headers=headers, params=params)

    return json.loads(response.text)

def calculate_leverage(position, account_info):
    symbol = position['symbol']
    position_amt = float(position['positionAmt'])
    mark_price = float(position['markPrice'])
    position_value = position_amt * mark_price

    # Assuming margin balance is in the account_info response
    margin_balance = float(account_info['totalMarginBalance'])  # Replace with actual field

    leverage = position_value / margin_balance
    return leverage

# Example usage:
positions = get_positions(api_key, api_secret)
account_info = get_account_info(api_key, api_secret)

print(positions)
print(account_info)

for position in positions:
    leverage = calculate_leverage(position, account_info)
    print(f"Symbol: {position['symbol']}, Leverage: {leverage}")