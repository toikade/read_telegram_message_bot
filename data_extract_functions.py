import telethon
from telethon.sync import TelegramClient, events
import datetime
import re
from utilities import get_number_from_str, get_next_line_items, check_lines_with_numbers, modify_extracted_data_body, block_contains_usd_or_usdt, get_binance_futures_asset_list_from_file, extract_entry_values_from_harrisons_data_block
from test import extract_numbers_after_targ


api_id = '21243794'
api_hash = '2a1ef85eff1fe10eb27560df055b1746'
bot_token = '6379620803:AAEaLOHQM6Zeo3niZFDDDjS4NnkH1S2NqqM'  #'your_bot_token'

#function to extract trade from ai crypto channel
binance_asset_list = get_binance_futures_asset_list_from_file()
#dict to hold extracted data
tradeData = {}
def  extract_signal_data_from_ai_crypto(text):
    if ('🟩' in str(text)) or ('🟥' in str(text)):
        ticker = re.findall(r'\#\w+', text)    #get ticker
        tradeData['ticker'] = ticker[0][1:]    #add ticker to dict
        lever = re.findall(r'\bx\w+', text)     #get leverage
        tradeData['leverage'] = lever[0][1:]   #add leverage to dict
        #print(message)
        #print(message.sender_id)
        #print(message.date, ':', text)
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
            #bre
        #break   
            
# def extract_signal_data_from_sentinel(text):
#     # Remove leading and trailing whitespace characters
#     cleaned_block = text.strip()
#     # Skip empty blocks
#     if cleaned_block:
#         #check the block contains trading data
#         data_block = check_lines_with_numbers(cleaned_block)
#         #print(data_block)
#         if data_block:
#             #initialize data dict
#             tradeData = {}
#             error_counter = 0
#             try:
#                 ticker = re.findall(r'\#\w+', data_block)    #get ticker
#                 ticker = str(ticker[0][1:]+'USDT')
#                 print(ticker)
#                 tradeData['ticker'] = ticker    #add ticker to dict
#                 lines = data_block.splitlines()       #split lines wrt to \n
#                 #lines = [i for i in lines if i != '']   # filter to remove empty items
    
#                 #print(lines)
#                 entry_and_target = get_next_line_items(lines)
#                 #get side from lines
#                 tradeData['side'] = [i for i in lines if i.lower()=='long' or i.lower()=='short'][0]
#                 #get leverage from lines
#                 tradeData['leverage'] = [get_number_from_str(line) for line in lines if 'Leverage' in line][0]
#                 #get entry from entry_and_target which returns list
#                 tradeData['entry'] = entry_and_target[0]
#                 #get targets from entry_and_target from list index 1
#                 tradeData['targets'] = entry_and_target[1]
#                 #get stop assuming its always last value in lines
#                 tradeData['stop'] = lines[-1]

#             except:
#                 pass
#             print(tradeData)
#             # sanitize the data and modify values so they are consistent and coherent
#             sanitized_data = modify_extracted_data_body(tradeData)
#             price_precised_data = calc_asset_precision(sanitized_data)
#             print(sanitized_data)
#             print(price_precised_data)
#             return sanitized_data
    
def extract_signal_data_from_harrisons(text):
    tradeData = {}
    # Extract TICKER
    # line = block_contains_usd_or_usdt(text)
    # line_without_usd = re.sub(r'(usdt|usd)', '', line, flags=re.IGNORECASE)
    # # Extract all alphanumeric characters from the remaining line
    # alphanumeric_chars = re.findall(r'[A-Za-z0-9]+', line_without_usd)
   
    # asset_string = ''.join(alphanumeric_chars)

    # concatenated_string = asset_string + 'USDT'
    # ticker =  concatenated_string
    # tradeData['ticker'] = ticker
    # print(ticker)
    #========================================================== 
    # Extract ENTRY prices 
    # tradeData['entries'] = extract_entry_values_from_harrisons_data_block(text)

    #========================================================== 
    # Extract TARGET prices
    tradeData['targets'] = extract_numbers_after_targ(text)
    #==========================================================         
    # # Extract SIDE (LONG/SHORT)
    # side_match = re.search(r'(LONG|SHORT)', text, re.IGNORECASE)
    # if side_match:
    #     tradeData['side'] = side_match.group(0).upper()  # Ensure consistent case in output
    #========================================================== 
    # # Extract leverage
    # leverage_match = re.search(r'Leverage: (\d+)x', text)
    # if leverage_match:
    #     tradeData['leverage'] = leverage_match.group(1)

    # # Extract target prices
    # target_match = re.findall(r'Target:\s*\d+\)\s*([\d.]+)', text)
    # if target_match:
    #     tradeData['targets'] = target_match

    # # Extract stop loss
    # stop_loss_match = re.search(r'StopLoss: ([\d.]+)', text)
    # if stop_loss_match:
    #     tradeData['stop'] = stop_loss_match.group(1)

    return tradeData

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
        


text = """#LINK/USDT 

Exchanges: Binance Futures, ByBit USD

Signal Type: LONG
Leverage: Cross 20X

Amount: 5.0%

Entry Targets: 16.60

Take Profit Targets:

1) 17.30 (75%) 
2) 19.00 (25%) 


Stop Targets: 16.00"""      

extract_signal_data_from_harrisons(text)