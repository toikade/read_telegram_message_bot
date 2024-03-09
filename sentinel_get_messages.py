import telethon
from telethon.sync import TelegramClient, events
import datetime
import re

api_id = '21243794'
api_hash = '2a1ef85eff1fe10eb27560df055b1746'
bot_token = '6379620803:AAEaLOHQM6Zeo3niZFDDDjS4NnkH1S2NqqM'  #'your_bot_token'


with TelegramClient('test', api_id, api_hash) as client:
    chat_entity = client.get_input_entity('t.me/SentinelCrypto')
    print(chat_entity.channel_id)
    #get the messages for today
    for message in client.iter_messages(chat_entity, offset_date=datetime.date.today(), reverse=True):
        #dictionary where all scraped data will be stored
        # print(type(message.text))
        test_msg = "['Binance Futures, ByBit USDT, KuCoin Futures, OKX Futures', '#ENS/USDT Closed at stoploss after reaching take profit ⚠']"
        pattern = r"\b" + re.escape("futures") + r"\b"
        #pattern = re.compile(r'(?i)(?=.*\bprofit\b)(?=.*\bfutures\b)')
        match = re.search(pattern, message.text, re.IGNORECASE)
        #match = pattern.search(message.text)
        #print(match)
        if(not match):
            tradeData = {}
            ticker = re.findall(r'\#\w+', message.text)    #get ticker
            ticker = str(ticker[0][1:]+'USDT')
            print(ticker)
            tradeData['ticker'] = ticker    #add ticker to dict
            lines = message.text.splitlines()
            # for line in lines:
            print(len(lines))
            #     #print(message.text)
            #     
            #print(lines)
            indexOfLastLine = len(lines)-1
            tradeData['side'] = lines[1]
            tradeData['leverage'] = lines[2].split()[1][:-1]
            tradeData['entry'] = lines[5:7]
            tradeData['targets'] = lines[9:indexOfLastLine-2]
            tradeData['stop'] = lines[-1]
            print(tradeData)
            print('-'*50)
                
                