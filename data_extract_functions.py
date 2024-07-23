import telethon
from telethon.sync import TelegramClient, events
import datetime
import re
from utilities import get_number_from_str, get_next_line_items, check_lines_with_numbers, extract_target_values_from_harrisons_data_block  
from utilities import modify_extracted_data_body, get_binance_futures_asset_list_from_file, extract_entry_values_from_harrisons_data_block
from utilities import extract_stop_value_from_harrisons_data_block, get_value_change_amount_from_percentage, extract_leverage_value_from_harrisons_data_block
from utilities import extract_ticker_from_harrisons_data_block, get_binance_futures_current_market_price_from_file, logger, modify_extracted_data_body, validate_data
from utilities import filter_text_with_numbers, get_symbol_market_value
from binance_utilities import get_current_price
#from test import process_lines


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
    
def extract_signal_data_from_harrisons(block):
    #a variable to hold text after confirmed to contain wanted numbers
    text = ''
    # Remove leading and trailing whitespace characters
    cleaned_block = block.strip()
    # Skip empty blocks
    if cleaned_block:
        #print(cleaned_block)
        data_block = filter_text_with_numbers(cleaned_block)
        #print(data_block)
        if not data_block:
            return
        #if the block is clean and contains the wanted numbers keep it in text
        text = data_block
    
    #a dict to store the data extracted and to be returned
    tradeData = {}
    # Extract TICKER
    
    tradeData['ticker'] = extract_ticker_from_harrisons_data_block(text)
    ticker = extract_ticker_from_harrisons_data_block(text)
    #========================================================== 
    # Extract mark_price or live market price 
    tradeData['mark_price'] = get_current_price(ticker)  # TEST OFFLINE with -- get_binance_futures_current_market_price_from_file(ticker)
    # try:
        
    # except ValueError as ve:
        #logger(text)
        # print(ve)
    #========================================================== 
    # Extract ENTRY prices 
    tradeData['entry'] = extract_entry_values_from_harrisons_data_block(text)
    print('ENTRY', tradeData['entry'])
    #========================================================== 
    # Extract TARGET prices
    tradeData['targets'] = extract_target_values_from_harrisons_data_block(text)
    targets = tradeData['targets']
    
    #==========================================================   

    # Extract leverage
    tradeData['leverage'] = extract_leverage_value_from_harrisons_data_block(text)
    #==========================================================
    # Extract SIDE (LONG/SHORT)
    entry_value = tradeData['entry'][-1] #get the last value of the entries
    target_value = targets[-1]
    try:
        if (float(entry_value) - float(target_value)) >0: #if entry price is higher than stop price
            tradeData['side'] = 'SHORT'
        else:
            tradeData['side'] = 'LONG'
    except ValueError as ve:
        print(ve)
    #========================================================== 
    # Extract STOP LOSS
    try:
        stop_value = extract_stop_value_from_harrisons_data_block(text)[0]
        entry_value = tradeData['entry'][-1] #get the last value of the entries
        side = tradeData['side']  #use the market side to calculate stop from [percentage]
    
    
        if '%' in stop_value:
            newChangeValue = 0
            match = re.search(r'(\d+(\.\d+)?)\s*%', stop_value) #filter out the %
            if match:
                percentage_number = match.group(1)
                #print('PERC', percentage_number)
                #get the stoploss value from the percentage given
            newChangeValue = get_value_change_amount_from_percentage(percentage_number, entry_value, side)
            tradeData['stop'] = newChangeValue
            #print('NEWSTOP', percentage_number, newChangeValue)
        else:
            tradeData['stop'] = stop_value
    except TypeError as e:
        print(e)
    except ValueError as ve:
        print(ve)
    except KeyError as ke:
        print(ke)
    #print('STOP', tradeData['stop'])
    #========================================================== 
    #SANITIZE Data to make sure the decimals are respected
    tradeData = modify_extracted_data_body(tradeData)
    #==========================================================
    #VALIDATE Data to make sure it meets the criteria of the different values
    tradeData = validate_data(tradeData)
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
        


text = """⚡️⚡️#SOL/USDT⚡️⚡️

LONG

LEVERAGE : Cross 50x


Entry target's :

1) 178.30
2) 176.00


Take-profit targets:

1) 182
2) 186
3) 192
4) 200

Stop Target: 174

Put 1% dep only"""      

#print(extract_signal_data_from_harrisons(text))