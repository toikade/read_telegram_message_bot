from binance.client import Client
from decouple import config

# Replace with your actual API keys
# Re-importing credentials inside the process
api_key = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
api_secret = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)

# Initialize the Binance client (testnet=True for demo account)
client = Client(api_key, api_secret, testnet=True)

# Fetch all open futures positions
positions = client.futures_position_information()

# Print all open positions
for position in positions:
    if float(position['positionAmt']) != 0:
        #print(position)
        print(f"Symbol: {position['symbol']}, Position: {position['positionAmt']} {position['positionSide']}, Entry Price: {position['entryPrice']}, Leverage: {position['leverage']}")

# Fetch account information (example for futures)
account_info = client.futures_account()

# Print margin balance and more
print("Futures Account Info:")
print(f"Margin Balance: {account_info['totalMarginBalance']}")
print(f"Total Unr. Profit: {account_info['totalUnrealizedProfit']}")
