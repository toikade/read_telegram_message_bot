import time
import json
import requests
import hmac
import hashlib
import multiprocessing
import os
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

# Function to place an order
def place_order(symbol, side, order_type, quantity, price=None, stop_price=None):
    endpoint = '/fapi/v1/order'
    url = BASE_URL + endpoint

    params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'timeInForce': 'GTC',
        'quantity': quantity,
        'timestamp': int(time.time() * 1000),
        'recvWindow': 5000
    }

    if price:
        params['price'] = price
    if stop_price:
        params['stopPrice'] = stop_price

    params['signature'] = create_signature(params, API_SECRET)

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.post(url, headers=headers, params=params)
    print(f"Order response for {symbol}: {response.json()}")
    return response.json()

# Function to cancel an order
def cancel_order(symbol, order_id):
    endpoint = '/fapi/v1/order'
    url = BASE_URL + endpoint

    params = {
        'symbol': symbol,
        'orderId': order_id,
        'timestamp': int(time.time() * 1000),
        'recvWindow': 5000
    }

    params['signature'] = create_signature(params, API_SECRET)

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.delete(url, headers=headers, params=params)
    print(f"Cancel order response for {symbol}: {response.json()}")
    return response.json()

def listener_process(queue):
    import asyncio
    import websockets
    from decouple import config

    # Re-importing credentials inside the process
    API_KEY = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
    API_SECRET = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)
    BASE_URL = 'https://testnet.binancefuture.com'

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

    async def run_websocket(listen_key):
        uri = f"wss://stream.binancefuture.com/ws/{listen_key}"

        async with websockets.connect(uri) as websocket:
            print("WebSocket connection established")
            try:
                while True:
                    data = await websocket.recv()
                    print(f"WebSocket message received: {data}")
                    queue.put(data)
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

    asyncio.run(listen_and_renew())

def main():
    # Create a queue for communication
    queue = multiprocessing.Queue()

    # Dictionary to track open orders
    open_orders = {}

    # Start the listener process
    listener = multiprocessing.Process(target=listener_process, args=(queue,))
    listener.start()

    # Place test limit orders for multiple symbols
    orders = [
        {"symbol": "BTCUSDT", "side": "BUY", "quantity": 0.002, "price": 58200.0},
        {"symbol": "ETHUSDT", "side": "SELL", "quantity": 0.05, "price": 2600.0}
    ]

    for order in orders:
        response = place_order(order["symbol"], order["side"], 'LIMIT', order["quantity"], order["price"])
        if response['status'] == 'NEW':
            open_orders[response['clientOrderId']] = {
                'symbol': order['symbol'],
                'side': order['side'],
                'quantity': order['quantity'],
                'price': order['price'],
                'take_profit_order_id': None,
                'stop_order_id': None
            }
            print(f"Open orders updated: {json.dumps(open_orders, indent=4)}")  # Debugging print

    # Listen for updates from the listener process
    while True:
        try:
            data = queue.get()
            message = json.loads(data)

            # Handle order updates
            if message['e'] == 'ORDER_TRADE_UPDATE':
                order_info = message['o']
                client_order_id = order_info['c']
                symbol = order_info['s']
                side = order_info['S']
                exec_price = float(order_info['L'])
                exec_qty = float(order_info['q'])

                if order_info['X'] == 'FILLED' and client_order_id in open_orders:
                    # Place take profit and stop loss orders
                    take_profit_price = round(exec_price * 1.04, 2) if side == 'BUY' else round(exec_price * 0.96, 2)
                    stop_price = round(exec_price * 0.96, 2) if side == 'BUY' else round(exec_price * 1.04, 2)

                    take_profit_order = place_order(
                        symbol,
                        'SELL' if side == 'BUY' else 'BUY',
                        'TAKE_PROFIT_MARKET',
                        exec_qty,
                        stop_price=take_profit_price
                    )

                    stop_order = place_order(
                        symbol,
                        'SELL' if side == 'BUY' else 'BUY',
                        'STOP_MARKET',
                        exec_qty,
                        stop_price=stop_price
                    )

                    # Update open_orders with new order IDs
                    open_orders[client_order_id]['take_profit_order_id'] = take_profit_order['clientOrderId']
                    open_orders[client_order_id]['stop_order_id'] = stop_order['clientOrderId']
                    print(f"Open orders updated: {json.dumps(open_orders, indent=4)}")  # Debugging print

            # Handle cancellation if one of the orders gets filled
            if message['e'] == 'ORDER_TRADE_UPDATE':
                order_info = message['o']
                client_order_id = order_info['c']
                status = order_info['X']

                for parent_order_id, orders in open_orders.items():
                    if orders['take_profit_order_id'] == client_order_id or orders['stop_order_id'] == client_order_id:
                        if status == 'FILLED':
                            # Cancel the other order
                            other_order_id = orders['stop_order_id'] if orders['take_profit_order_id'] == client_order_id else orders['take_profit_order_id']
                            cancel_order(symbol, other_order_id)

                            # Remove parent order from open orders as it is fully managed now
                            del open_orders[parent_order_id]
                            print(f"Open orders updated: {json.dumps(open_orders, indent=4)}")  # Debugging print
                        break

        except Exception as e:
            print(f"Error processing data: {e}")

if __name__ == '__main__':
    main()
