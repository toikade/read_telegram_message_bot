from binance.client import Client
from decouple import config

def place_orders(data, take_profit_index=None):
    # Load your API key and secret from environment variables or a .env file
    api_key = config('BINANCE_FUTURES_DEMO_API_KEY',cast = str)
    api_secret = config('BINANCE_FUTURES_DEMO_SECRET', cast = str)

    print(f"API Key: {api_key}")
    print(f"API Secret: {api_secret}")

    # Initialize the Binance client
    client = Client(api_key, api_secret)

    # Extract data
    ticker = data['ticker']
    entry_prices = data['entry']
    targets = data['targets']
    leverage = int(data['leverage'][0])
    side = data['side']
    quantity_usdt = 10  # Amount to be used per trade in USDT

    # Determine order side
    order_side = Client.SIDE_BUY if side == 'LONG' else Client.SIDE_SELL

    # Set leverage
    client.futures_change_leverage(symbol=ticker, leverage=leverage)

    # Place limit orders for each entry price
    for entry_price in entry_prices:
        entry_price = float(entry_price)
        quantity = quantity_usdt / entry_price

        # Ensure the quantity is formatted correctly
        quantity = round(quantity, 3)  # Adjust precision as needed

        order = client.futures_create_order(
            symbol=ticker,
            side=order_side,
            type=Client.ORDER_TYPE_LIMIT,
            timeInForce=Client.TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=f'{entry_price:.6f}'
        )
        print(f"Entry order placed: {order}")

    # Place stop order
    stop_price = float(data['stop'])
    stop_side = Client.SIDE_SELL if side == 'LONG' else Client.SIDE_BUY

    stop_order = client.futures_create_order(
        symbol=ticker,
        side=stop_side,
        type=Client.ORDER_TYPE_STOP_MARKET,
        quantity=quantity,
        stopPrice=f'{stop_price:.6f}'
    )
    print(f"Stop order placed: {stop_order}")

    # Place take profit orders
    place_take_profit_orders(client, ticker, targets, quantity, side, take_profit_index)

def place_take_profit_orders(client, ticker, targets, total_quantity, side, index=None):
    # Determine order side for take profit
    take_profit_side = Client.SIDE_SELL if side == 'LONG' else Client.SIDE_BUY

    if index is not None:
        # Ensure the index is within range
        if index < 0 or index >= len(targets):
            raise ValueError("The provided index is out of range for the targets list.")

        # Calculate the quantity for the specific target
        target_price = float(targets[index])
        
        # Ensure the quantity is formatted correctly
        quantity = round(total_quantity, 3)  # Adjust precision as needed

        order = client.futures_create_order(
            symbol=ticker,
            side=take_profit_side,
            type=Client.ORDER_TYPE_LIMIT,
            timeInForce=Client.TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=f'{target_price:.6f}'
        )
        print(f"Take profit order placed: {order}")
    else:
        # Calculate the quantity per target
        num_targets = len(targets)
        quantity_per_target = total_quantity / num_targets

        # Place limit orders for each target price
        for target_price in targets:
            target_price = float(target_price)
            
            # Ensure the quantity is formatted correctly
            quantity = round(quantity_per_target, 3)  # Adjust precision as needed

            order = client.futures_create_order(
                symbol=ticker,
                side=take_profit_side,
                type=Client.ORDER_TYPE_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=f'{target_price:.6f}'
            )
            print(f"Take profit order placed: {order}")

# Example usage
data = {
    'ticker': 'JASMYUSDT',
    'mark_price': '0.029950',
    'entry': ['0.02815', '0.02800'],
    'targets': ['0.02955', '0.02965', '0.02975', '0.03'],
    'leverage': ['20'],
    'side': 'LONG',
    'stop': '0.0255'
}

# Specify the index of the target to be considered for the take profit order, or None for all targets
take_profit_index = 2  # Set to None to consider all targets

place_orders(data, take_profit_index)
