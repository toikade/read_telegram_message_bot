import asyncio
import websockets
import json

async def main():
    uri = "wss://stream.binance.com:9443/ws/bomeusdt@depth"

    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            data = json.loads(data)

            # Extract the best bid and ask prices
            best_bid = float(data['b'][0][0])
            best_ask = float(data['a'][0][0])
            spread = best_ask - best_bid
            print(f"Best Buy(Bid): {best_bid}, Best Sell(Ask): {best_ask}, Spread:{spread}")

asyncio.run(main())
