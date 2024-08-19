import time
import asyncio
import json
import websockets
import requests
import hmac
import hashlib
from decouple import config

# Binance API credentials
API_KEY = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
API_SECRET = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)

# Base URL for Binance Futures testnet API
BASE_URL = 'https://testnet.binancefuture.com'

# Function to generate the signature
def create_signature(params, secret):
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# Function to get a listen key for user data stream
def get_listen_key():
    endpoint = '/fapi/v1/listenKey'
    url = BASE_URL + endpoint

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.post(url, headers=headers)
    data = response.json()
    print("Listen key received:", data)
    return data['listenKey']

# Function to renew listen key
def renew_listen_key(listen_key):
    endpoint = '/fapi/v1/listenKey'
    url = BASE_URL + endpoint

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    params = {'listenKey': listen_key}

    response = requests.put(url, headers=headers, params=params)
    data = response.json()
    print("Listen key renewed:", data)
    return data['listenKey']

# Function to place a limit order (for testing purposes)
def place_limit_order(symbol, side, quantity, price):
    endpoint = '/fapi/v1/order'
    url = BASE_URL + endpoint

    params = {
        'symbol': symbol,
        'side': side,
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': quantity,
        'price': price,
        'timestamp': int(time.time() * 1000),
        'recvWindow': 5000
    }

    params['signature'] = create_signature(params, API_SECRET)

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.post(url, headers=headers, params=params)
    print("Order response:", response.json())
    return response.json()

async def run_websocket(listen_key):
    uri = f"wss://stream.binancefuture.com/ws/{listen_key}"

    async with websockets.connect(uri) as websocket:
        print("WebSocket connection established")
        try:
            while True:
                data = await websocket.recv()
                print(f"WebSocket message received: {data}")
                # Process the data as needed
                message = json.loads(data)
                if message['e'] == 'ORDER_TRADE_UPDATE':
                    print(f"Order update: {message}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("WebSocket connection closed")

async def listen_and_renew():
    listen_key = get_listen_key()
    listen_key_expiration = time.time() + 24 * 60 * 60  # Listen key expires in 24 hours

    while True:
        try:
            await run_websocket(listen_key)
        except Exception as e:
            print(f"WebSocket error: {e}")
            await asyncio.sleep(5)  # Retry after 5 seconds

        time_remaining = listen_key_expiration - time.time()
        if time_remaining < 60 * 60:  # Renew listen key if less than 1 hour remaining
            listen_key = renew_listen_key(listen_key)
            listen_key_expiration = time.time() + 24 * 60 * 60

async def main():
    await listen_and_renew()

if __name__ == '__main__':
    asyncio.run(main())
