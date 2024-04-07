import telethon
from telethon.sync import TelegramClient, events
from datetime import date, timedelta
import datetime
import re

api_id = '21243794'
api_hash = '2a1ef85eff1fe10eb27560df055b1746'
bot_token = '6379620803:AAEaLOHQM6Zeo3niZFDDDjS4NnkH1S2NqqM'  #'your_bot_token'


with TelegramClient('test', api_id, api_hash) as client:
    chat_entity = client.get_input_entity('https://t.me/HarrisonFutures1')
    print(chat_entity.channel_id)
    #get the date of yesterday
    yesterday = date.today() - timedelta(days = 500)
    #get today's date
    today = datetime.date.today()
    #get the messages for today
    for message in client.iter_messages(chat_entity, offset_date=yesterday, reverse=True):
        #dictionary where all scraped data will be stored
        print(message.date)
        print(message.text)
        print('='*30)
        sep = '='*30
        try:
            with open('harrisonfutures.txt', 'a',  encoding='utf-8') as file:  # Open file in append mode
                for line in message.text.splitlines():
                    file.write(f'{line}\n')
                file.write(f'{sep}\n')
        except AttributeError:
            continue
            with open('sentinel.txt', 'a',  encoding='utf-8') as file:  # Open file in append mode
                for line in message.text.splitlines():
                    file.write(line)

        # test_msg = "['Binance Futures, ByBit USDT, KuCoin Futures, OKX Futures', '#ENS/USDT Closed at stoploss after reaching take profit ⚠']"
        # pattern = r"\b" + re.escape("futures") + r"\b"
        # #pattern = re.compile(r'(?i)(?=.*\bprofit\b)(?=.*\bfutures\b)')
        # match = re.search(pattern, message.text, re.IGNORECASE)
        # #match = pattern.search(message.text)
        # #print(match)
        # if(not match):
        #     tradeData = {}
        #     ticker = re.findall(r'\#\w+', message.text)    #get ticker
        #     ticker = str(ticker[0][1:]+'USDT')
        #     print(ticker)
        #     tradeData['ticker'] = ticker    #add ticker to dict
        #     lines = message.text.splitlines()
        #     # for line in lines:
        #     print(len(lines))
        #     #     #print(message.text)
        #     #     
        #     #print(lines)
        #     indexOfLastLine = len(lines)-1
        #     tradeData['side'] = lines[1]
        #     tradeData['leverage'] = lines[2].split()[1]    #tradeData['leverage'] = lines[2].split()[1][:-1]
        #     tradeData['entry'] = lines[5:7]
        #     tradeData['targets'] = lines[9:indexOfLastLine-2]
        #     tradeData['stop'] = lines[-1]
        #     print(tradeData)
        #     print('-'*50)
                
                