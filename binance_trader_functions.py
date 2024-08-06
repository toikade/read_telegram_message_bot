import requests
import time
import hmac
import hashlib
from decouple import config

# Binance API credentials
API_KEY = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
API_SECRET = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)

# Base URL for Binance Futures API
BASE_URL = 'https://testnet.binancefuture.com'

# Function to generate the signature
def create_signature(params, secret):
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

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

# Function to set leverage for a symbol
def set_leverage(symbol, leverage):
    endpoint = '/fapi/v1/leverage'
    url = BASE_URL + endpoint

    params = {
        'symbol': symbol,
        'leverage': leverage,
        'timestamp': int(time.time() * 1000)
    }

    # Create signature
    params['signature'] = create_signature(params, API_SECRET)

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.post(url, headers=headers, params=params)
    try:
        return response.json()
    except ValueError:
        print(f"Error parsing JSON response: {response.text}")
        return None

# Function to calculate the quantity to be traded based on the USDT amount and price
def calculate_quantity(usdt_amount, price, step_size):
    quantity = usdt_amount / price
    # Adjust quantity to the correct precision
    precision = len(str(step_size).split('.')[1])
    quantity = round(quantity // step_size * step_size, precision)
    return quantity

# A function to check the status of an order
def check_order_status(symbol, order_id):
    """Checks the status of an order on Binance.

    Args:
        symbol: The trading symbol (e.g., BTCUSDT).
        order_id: The order ID to check.

    Returns:
        A dictionary containing the order status and other details.
    """

    endpoint = '/fapi/v1/order'
    url = BASE_URL + endpoint

    params = {
        'symbol': symbol,
        'orderId': order_id,
        'timestamp': int(time.time() * 1000)
    }

    # Create signature
    params['signature'] = create_signature(params, API_SECRET)

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.get(url, headers=headers, params=params)
    try:
        return response.json()
    except ValueError:
        print(f"Error parsing JSON response: {response.text}")
        return None
    
# A function to cancel an order    
def cancel_order(symbol, order_id):
    """Cancels an order on Binance.

    Args:
        symbol: The trading symbol (e.g., BTCUSDT).
        order_id: The order ID to cancel.

    Returns:
        A dictionary containing the cancellation response.
    """

    endpoint = '/fapi/v1/order/cancel'
    url = BASE_URL + endpoint

    params = {
        'symbol': symbol,
        'orderId': order_id,
        'timestamp': int(time.time() * 1000)
    }

    # Create signature
    params['signature'] = create_signature(params, API_SECRET)

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.delete(url, headers=headers, params=params)
    try:
        return response.json()
    except ValueError:
        print(f"Error parsing JSON response: {response.text}")
        return None
    

# Function to place a limit order
def place_limit_order(symbol, side, usdt_amount, price=None, tp_price=None, sl_price=None):
    endpoint = '/fapi/v1/order'
    url = BASE_URL + endpoint

    # Get the current price if not provided
    if price is None:
        price = get_current_price(symbol)

    # Get symbol info for precision and minimum notional
    symbol_info = get_symbol_info(symbol)
    if not symbol_info:
        print(f"Symbol info not found for {symbol}")
        return None

    step_size = float(symbol_info['filters'][2]['stepSize'])
    min_notional_filter = next((f for f in symbol_info['filters'] if f['filterType'] == 'MIN_NOTIONAL'), None)

    if not min_notional_filter:
        print(f"Min notional filter not found for {symbol}")
        return None

    min_notional = float(min_notional_filter['notional'])

    # Calculate the quantity based on the USDT amount
    quantity = calculate_quantity(usdt_amount, price, step_size)

    # Ensure the trade value meets the minimum notional requirement
    trade_value = quantity * price
    if trade_value < min_notional:
        required_quantity = min_notional / price
        quantity = calculate_quantity(required_quantity * price, price, step_size)
        print(f"Adjusted quantity to meet minimum notional: {quantity}")

    # Print the calculated quantity
    print(f"Calculated quantity: {quantity}")

    # Ensure quantity is greater than zero
    if quantity <= 0:
        print(f"Calculated quantity is less than or equal to zero. Adjust the USDT amount or check the step size.")
        return None

    # Order parameters
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'LIMIT',
        'timeInForce': 'GTC',  # Good Till Cancel
        'quantity': quantity,  # Adjusted to correct precision
        'price': round(price, 2),  # Assuming 2 decimal places for price
        'reduceOnly': 'false',  # Set the reduce-only parameter
        'timestamp': int(time.time() * 1000)
    }

    # Create signature
    params['signature'] = create_signature(params, API_SECRET)

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.post(url, headers=headers, params=params)
    try:
        primary_order_id = None
        tp_order_id = None
        sl_order_id = None
        order_response = response.json()
        if order_response and 'orderId' in order_response:
            primary_order_id = order_response['orderId']
            client_order_id = order_response['clientOrderId']
            
            # Place TP and SL orders if specified
            if tp_price:
                # Check if primary order is still open before placing TP
                is_primary_open = check_order_status(symbol, primary_order_id)
                if is_primary_open:
                    tp_params = {
                        'symbol': symbol,
                        'side': 'SELL' if side == 'BUY' else 'BUY',
                        'type': 'TAKE_PROFIT_MARKET',
                        'quantity': quantity,
                        'stopPrice': round(tp_price, 2),
                        'reduceOnly': 'true',
                        'newClientOrderId': client_order_id + '_TP',
                        'closePosition': True,  # Ensure TP order closes the position
                        'timestamp': int(time.time() * 1000)
                    }
                tp_params['signature'] = create_signature(tp_params, API_SECRET)
                tp_response = requests.post(url, headers=headers, params=tp_params)
                if tp_response.json().get('code') == 0:
                    tp_order_id = tp_response.json()['orderId']
                else:
                    print(f"Failed to place TP order: {tp_response.text}")


            if sl_price:
                # Check if primary order is still open before placing SL
                is_primary_open = check_order_status(symbol, primary_order_id)
                if is_primary_open:
                    sl_params = {
                        'symbol': symbol,
                        'side': 'SELL' if side == 'BUY' else 'BUY',
                        'type': 'STOP_MARKET',
                        'quantity': quantity,
                        'stopPrice': round(sl_price, 2),
                        'reduceOnly': 'true',
                        'newClientOrderId': client_order_id + '_SL',
                        'closePosition': True,  # Ensure SL order closes the position
                        'timestamp': int(time.time() * 1000)
                    }
                sl_params['signature'] = create_signature(sl_params, API_SECRET)
                sl_response = requests.post(url, headers=headers, params=sl_params)
                if sl_response.json().get('code') == 0:
                    sl_order_id = sl_response.json()['orderId']
                else:
                    print(f"Failed to place SL order: {sl_response.text}")

        return order_response
    except ValueError:
        print(f"Error parsing JSON response: {response.text}")
        return None

# Main function
def main():
    symbol = 'BTCUSDT'
    side = 'BUY'  # 'BUY' to open a long position, 'SELL' to open a short position
    usdt_amount = 145.0  # Amount in USDT to use for the trade
    leverage = 67  # Leverage to be used for the trade

    # Set leverage for the symbol
    leverage_response = set_leverage(symbol, leverage)
    if 'leverage' not in leverage_response:
        print(f"Failed to set leverage: {leverage_response}")
        return

    # Get the current price of the symbol
    current_price = get_current_price(symbol)

    # Calculate TP and SL prices
    tp_price = current_price * 1.005  # Example: 5% above current price for TP
    sl_price = current_price * 0.98  # Example: 5% below current price for SL

    # Place the limit order with TP and SL
    order_response = place_limit_order(symbol, side, usdt_amount, price=current_price, tp_price=tp_price, sl_price=sl_price)

    if order_response:
        # Check for specific error codes and handle them
        if order_response.get('code') == -4164:
            symbol_info = get_symbol_info(symbol)
            min_notional_filter = next((f for f in symbol_info['filters'] if f['filterType'] == 'MIN_NOTIONAL'), None)
            min_notional = float(min_notional_filter['notional'])
            min_required_amount = min_notional
            print(f"Order's notional value is too low. Minimum required notional value is {min_notional} USDT.")
            print(f"Please use at least {min_required_amount:.6f} {symbol[:-4]} to meet the minimum notional value.")
        elif order_response.get('code') == -1111:
            print(f"Precision is over the maximum defined for this asset.")
        elif order_response.get('code') == -4003:
            print(f"Quantity less than or equal to zero. Adjust the USDT amount or check the step size.")
        else:
            print(order_response)
    else:
        print("No response from the server or an error occurred.")

if __name__ == '__main__':
    main()