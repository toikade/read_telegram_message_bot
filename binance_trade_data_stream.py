import hmac
import hashlib
import json
import time
import requests
import websocket
from threading import Thread
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
    url = f'{BASE_URL}/fapi/v1/listenKey'
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    response = requests.post(url, headers=headers)
    data = response.json()
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

# Function to monitor order status
def monitor_order_status(listen_key):
    ws_url = f'wss://fstream.binance.com/ws/{listen_key}'

    def on_message(ws, message):
        data = json.loads(message)
        print(f"WebSocket message received: {data}")
        if data.get('e') == 'ORDER_TRADE_UPDATE':
            order_id = data['o']['i']
            order_status = data['o']['X']
            print(f"Order ID: {order_id} - Status: {order_status}")
            if order_status == 'FILLED':
                print(f"Order {order_id} filled.")

    def on_open(ws):
        print("WebSocket connection opened")

    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print(f"WebSocket connection closed with status: {close_status_code}, message: {close_msg}")

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_open=on_open,
        on_error=on_error,
        on_close=on_close
    )

    # Adding a heartbeat to keep the connection alive
    def send_heartbeat(ws):
        while True:
            time.sleep(30)
            try:
                ws.send(json.dumps({'event': 'ping'}))
            except Exception as e:
                print(f"Heartbeat error: {e}")
                break

    Thread(target=send_heartbeat, args=(ws,)).start()
    ws.run_forever()

# Function to run WebSocket listener in a separate thread
def start_monitoring(listen_key):
    thread = Thread(target=monitor_order_status, args=(listen_key,))
    thread.daemon = True
    thread.start()

# Main function
def main():
    symbol = 'BTCUSDT'
    side = 'BUY'
    quantity = 0.002  # Example quantity
    price = 61326.0  # Example price (adjust as necessary for testnet)

    # Get listen key
    listen_key = get_listen_key()
    print(f"Listen key: {listen_key}")

    # Start monitoring order updates
    start_monitoring(listen_key)

    # Place a test limit order (adjust parameters as necessary)
    place_limit_order(symbol, side, quantity, price)

    # Keep the main function running to allow continuous monitoring
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
