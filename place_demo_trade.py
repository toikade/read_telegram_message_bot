#import python-binance
from decouple import config
from binance.client import Client
import time
from get_asset_precision import get_asset_precision


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


def place_buy_sell_limit_order(symbol, side, quantity, price):

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            quantity=round(quantity, 4),
            price=price,
            timeInForce='GTC',
            #reduceOnly=True

        )
        limit_order_response.append(order)
        print(order)
        print(side, "order placed successfully:")
        print("Symbol:", order['symbol'])
        print("Order Type:", order['type'])
        print("Side:", order['side'])
        print("Quantity:", order['origQty'])
        print("Price:", order['price'])

    except Exception as e:
        print("Error placing test order:", e)
        return None

def place_stop_order(symbol, side, quantity, price):
    try:
        stop_loss_price = float(price)
        stop_loss_order = client.futures_create_order(
            symbol=symbol,
            side=side,  # Assuming you want to set a stop loss by selling
            type='STOP_MARKET',
            timeInForce = 'GTC',
            reduceOnly = True,
            quantity=round(quantity, 4),  # Round the quantity to 4 decimal places
            stopPrice=str(stop_loss_price)
        )
        print('Tp order placed succesfully')
        print(stop_loss_order)
    except Exception as e:
        print("Error placing tp order:", e)
        return None

if __name__ == "__main__":
    data_body = {'ticker': '1INCHUSDT', 'side': 'LONG', 'leverage': '20', 'entry': ['0.5400', '0.6200'], 'targets': ['0.63200', '0.6340', '0.6400', '0.6520', '0.6760'], 'stop': '0.4935'}
    #a list to hold the response of order
    limit_order_response = []
    # symbol = 'BTCUSDT'
    # side = 'BUY'
    asset_quantity_precision = get_asset_precision(data_body['ticker'])['quantityPrecision']
    notional = 150 # 0.001 BTC
    entry_price = data_body['entry'][0]  # Entry price
    # leverage = 100  # Leverage level
    quantity = float("{:0.0{}f}".format(notional/float(entry_price), asset_quantity_precision))
    # print(notional/int(entry_price))
    print('QUANT', quantity)
    

    # Step 1: Set leverage
    set_leverage(data_body['ticker'], data_body['leverage'])

    # Step 2: Place limit order
    # if side is long
    if data_body['side'] == 'BUY' or data_body['side'] == 'LONG':
        #binance recognizes BUY and SELL
        side = 'BUY'
        #start by buying
        place_buy_sell_limit_order(data_body['ticker'], side, quantity, entry_price)
        #wait for 2 seconds before setting sell price (tp)
        time.sleep(2)
        #get quantity to sell from order response from above
        sell_quantity = float(limit_order_response[0]['origQty'])
        #place an order to sell all and take all profits at TP1 (targets[0] )
        place_buy_sell_limit_order(data_body['ticker'], 'SELL', sell_quantity, str(min([float(x) for x in data_body['targets']])) )
        #wait 2 seconds before setting a Stop Loss
        time.sleep(2)
        place_stop_order(data_body['ticker'], 'SELL', sell_quantity, data_body['stop'])
    
    #if the side in data_body is short
    else:
        side = 'SELL'
        #start by selling
        place_buy_sell_limit_order(data_body['ticker'], side, quantity, entry_price)
        #wait 2 seconds before setting TP
        time.sleep(2)
        #get quantity to buy from order response from above
        sell_quantity = float(limit_order_response[0]['origQty'])
        #place an order to buy all and take all profits at TP1 (targets[0] )
        place_buy_sell_limit_order(data_body['ticker'], 'BUY', sell_quantity, str(max([float(x) for x in data_body['targets']])) )
        #wait 2 seconds before setting SL
        time.sleep(2)
        #place a stop_market order by buying all
        place_stop_order(data_body['ticker'], 'BUY', sell_quantity, data_body['stop'])
    
   # place_limit_order(symbol,"SELL", 0.002, '71500.0')

    #place stop order
    #place_stop_order(symbol, "SELL", 0.004, '69000.0')