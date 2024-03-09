import telethon
from telethon.sync import TelegramClient, events
import datetime
import re

api_id = '21243794'
api_hash = '2a1ef85eff1fe10eb27560df055b1746'
bot_token = '6379620803:AAEaLOHQM6Zeo3niZFDDDjS4NnkH1S2NqqM'  #'your_bot_token'

#function to extract trade from ai crypto channel
def  extract_signal_data_from_ai_crypto(text):
    if ('🟩' in str(text)) or ('🟥' in str(text)):
            ticker = re.findall(r'\#\w+', text)    #get ticker
            tradeData['ticker'] = ticker[0][1:]    #add ticker to dict
            lever = re.findall(r'\bx\w+', text)     #get leverage
            tradeData['leverage'] = lever[0][1:]   #add leverage to dict
            #print(message)
            print(message.sender_id)
            print(message.date, ':', text)
            print(ticker)
            print(lever)
            for line in text.splitlines():
                splitLine = line.split('-')
                if splitLine[0]!='':
                    # get the side
                    if splitLine[0][0] == '🟩':
                        side = 'Buy'
                        tradeData['side'] = side
                    if splitLine[0][0] == '🟥':
                        side = 'Sell'
                        tradeData['side'] = side
                    #get the entry values
                    if splitLine[0][0] == 'E':
                        entries = [splitLine[0][7:].strip(), splitLine[1][1:].strip()]
                        tradeData['entry'] = entries
                    #get the target values
                    if splitLine[0][0] == 'T':
                        targets = [splitLine[0][9:].strip(), splitLine[1].strip(), splitLine[2].strip(),
                                   splitLine[3].strip(), splitLine[4].strip()]
                        tradeData['targets'] = targets
                    #get the StopLoss
                    if splitLine[0][0] == 'S':
                        stopLoss = splitLine[0][11:]
                        tradeData['stop'] = stopLoss
                    #print(splitLine)
            print(tradeData)
            
            print('--'*30)
            #break
        #break
            
def extract_signal_data_from_sentinel(text):
    test_msg = "['Binance Futures, ByBit USDT, KuCoin Futures, OKX Futures', '#ENS/USDT Closed at stoploss after reaching take profit ⚠']"
    pattern = r"\b" + re.escape("futures") + r"\b"
    #pattern = re.compile(r'(?i)(?=.*\bprofit\b)(?=.*\bfutures\b)')
    match = re.search(pattern, text, re.IGNORECASE)
    #match = pattern.search(message.text)
    #print(match)
    if(not match):
        #tradeData = {}
        ticker = re.findall(r'\#\w+', text)    #get ticker
        ticker = str(ticker[0][1:]+'USDT')
        print(ticker)
        tradeData['ticker'] = ticker    #add ticker to dict
        lines = text.splitlines()
        # for line in lines:
        #     print(line)
        #     #print(message.text)
        #     
        #print(lines)
        tradeData['side'] = lines[1]
        tradeData['leverage'] = lines[2].split()[1][:-1]
        tradeData['entry'] = lines[5:7]
        tradeData['targets'] = lines[9:16]
        tradeData['stop'] = lines[-1]
    


# with TelegramClient('test', api_id, api_hash) as client:
#     chat_entity = client.get_input_entity('t.me/+6Lg31Rwf1UtlYWFk')
#     # get the messages for today and iterate over them
#     for message in client.iter_messages(chat_entity, offset_date=datetime.date.today(), reverse=True):
#         #dictionary where all scraped data will be stored
#         # print(type(message.text))
#         # print(message.text)
#         # print('-'*50)
#         tradeData = {}
#         raw_message = message.text
#         #extract_signal_data_from_ai_crypto(raw_message)
        


