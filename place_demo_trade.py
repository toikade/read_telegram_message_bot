#import python-binance
from decouple import config
from binance.client import Client


# Binance API key and secret
api_key = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
api_secret = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)

# Initialize the Binance Futures client
client = Client(api_key, api_secret, testnet=True)  # testnet=True for the Binance futures demo

def set_leverage(symbol, leverage):
    try:
        # Set leverage for the symbol
        client.futures_change_leverage(symbol=symbol, leverage=leverage)

        print(f"Leverage set to {leverage}x for symbol {symbol}")

    except Exception as e:
        print(f"Error: {e}")

def place_limit_order(symbol, side, quantity, price):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'
        )
        print("Test order placed successfully:")
        print("Symbol:", order['symbol'])
        print("Order Type:", order['type'])
        print("Side:", order['side'])
        print("Quantity:", order['origQty'])
        print("Price:", order['price'])

    except Exception as e:
        print("Error placing test order:", e)
        return None

if __name__ == "__main__":
    symbol = 'BTCUSDT'
    side = 'BUY'
    notional = 100  # 0.001 BTC
    entry_price = '47950'  # Entry price
    leverage = 100  # Leverage level
    quantity = float("{:0.0{}f}".format(notional/int(entry_price), 3))
    print(notional/int(entry_price))
    
    print(quantity)
    print(type(quantity))

    # Step 1: Set leverage
    set_leverage(symbol, leverage)

    # Step 2: Place limit order
    place_limit_order(symbol, side, quantity, entry_price)