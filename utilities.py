from decouple import config
from binance.client import Client

# Initialize Binance client
api_key = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
api_secret = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)
client = Client(api_key, api_secret, testnet=True)

def count_decimal_places(number):
    return len(str(number).split('.')[1])

def get_symbol_market_value(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    market_price = ticker['price']
    return market_price

# def get_symbol_market_value_and_divide_by_two(symbol):
#     # Get the market value of the asset
#     ticker = client.get_symbol_ticker(symbol=symbol)
#     ticker_value = ticker['price']
#     market_value = float(ticker_value)

#     #convert the string to a float and divide it by 2
#     divideBytwoPrice = float(market_value)/2

#     # Count of decimal places in market_value
#     market_value_decimal_places_count = count_decimal_places(market_value)
#     print('market_value_decimal_count', market_value_decimal_places_count)
#     # If decimal places in dividedByTwoPrice is greater than of market_value
#     if count_decimal_places(divideBytwoPrice) > market_value_decimal_places_count:
#         #round the number to the number of decimal places in the market value
#         divideBytwoPrice = round(divideBytwoPrice, market_value_decimal_places_count)

#     print('market_value', float(market_value))
#     return divideBytwoPrice

#a finction to determine the number of leading zeros in a decimal
def transform_number(number, leading_zeros_count):
    number = str(number)
    if leading_zeros_count == 0:
        transformed_number = '0' + '.' + number
    else:
        transformed_number = '0' + '.' + ('0'*leading_zeros_count) + number

    return transformed_number

def leading_zero_counter(number):
    strin = str(number)
    dot_index = 0
    zero_count = 0
    for idx, i in enumerate(strin):
        if strin[idx] == '.':
            dot_index = idx
        if idx > dot_index:
            if i != '0':
                break
            zero_count += 1

    return zero_count

#a function to return true if number has decimal
def has_decimal(number):
    str_number = str(number)
    return True if '.' in str_number else False

# a function to make sure a block of data is valid(has enough nbers to be trade the trade data)
def check_lines_with_numbers(text):
    lines = text.split('\n')
    count = 0

    #check if the 2nd to last line is SL so as to filter wanted data blocks
    if ('SL' in lines):
        for line in lines:
            # Check if the line contains a number (integer or decimal) and if the lines are not too long
            if any(char.isdigit() or char == '.' for char in line) and len(line)<15:
                count += 1
        
        if count >= 6:  # Return True if there are 6 or more lines with a number
            return text
        else:
            return 0
        
#get_number_from_str eg ('Leverage 20x')    
def get_number_from_str(text):
    num = ''
  
    for i in text:
            if i.isdigit():
                num += i   
    return num

# afunction to get entry and target values from the next lines dynamically
def get_next_line_items(text):
    lines = text        #was text.splitlines() but the caller fxn has already splitlines
    #print('here')
    #print (lines)
    start_index = 0
    
    return_arr = []
    for idx, line in enumerate(lines):
        #print(idx, line)
        for item in ['Entry', 'Targets']:
            if item in line:
                collected_items = []
                start_index = idx #get the index of entry
                #while line w start index+1 is not empty or the first character in the nextline is not a digit
                while (lines[start_index+1]):
                    #strip line to handle lines with a leading whitespace
                    second_condition = lines[start_index+1].strip()[0].isdigit() 
                    if not second_condition:    # if line is not a digit
                        break
                    else:
                        print('ln', lines[start_index+1])
                        collected_items.append(lines[start_index+1].strip())
                        start_index += 1
                return_arr.append(collected_items)
                break 
            
    
    return return_arr

#a function to modify(sanitize) data in data_body
def modify_extracted_data_body(data):
    #if ticker live market value is less than 1
    #ticker_market_value = get_symbol_market_value(data_body['ticker'])
    ticker_market_value = get_symbol_market_value(data['ticker'])    # placeholder test value
    print('ticker_value',ticker_market_value)
    ticker_market_value_on_2 = float(ticker_market_value)/2
    #count the number of leading zeros(function) in value
    leading_zero_count = leading_zero_counter(ticker_market_value_on_2)
    #if side is LONG
    if data['side'] == 'LONG':
        #if stopLoss has a decimal point
        if has_decimal(data['stop']):
            #return data bc all other values should be sanitized already
            print(data) 
            return data
        #else if there is no decimal in SL, other values are not sanitized
        else:
            #transform Sl by adding the leading zeros
            data['stop'] = str(transform_number(int(data['stop']), leading_zero_count))
            #store sanitized SL in a variable
            comparative_stop_loss = data['stop']
             #iterate over the data items
            
            for item in ['entry', 'targets']:
                for idx, elm in enumerate(data[item]):
                    #if elm has a decimal and is greater than SL(value is ok)
                    
                    if has_decimal(elm) and float(elm) >= float(comparative_stop_loss):
                        print('compSL', comparative_stop_loss)
                        continue
                    else:
                        #transform each element
                        transformed_elm = float(transform_number(int(elm), leading_zero_count))
                        print('trElm',transformed_elm)
                        #if elm is gt stop loss then it is correct since this is LONG
                        if transformed_elm >= float(comparative_stop_loss):
                        #convert transformed element to string and replace elm
                            data[item][idx] = str(transformed_elm)
                        else:
                        #multiply by 10 to shift 1dp to right and replace with str of elm
                            data[item][idx] = str(transformed_elm*10)
        print(data)
        return data

    #in case side is SHORT
    else: 
        #if smallest target has a decimal and the number is gt 1
        if has_decimal(data['targets'][-1]) and float(data['targets'][-1]) > 1:
            #return data body
            print(data)
            return data
        else:
            data['targets'][-1] = str(transform_number(int(data['targets'][-1]), leading_zero_count))
            #store sanitized value in a variable
            comparative_smallest_target = data['targets'][-1]
            #iterate over the data items
            
            for item in ['entry', 'targets']:
                for idx, elm in enumerate(data[item]):
                    #if elm has a decimal and is greater than Smallest target(value is ok)
                    if has_decimal(float(elm)) and float(elm) >= float(comparative_smallest_target):
                        continue
                    else:
                        #transform each element
                        transformed_elm = float(transform_number(int(elm), leading_zero_count))
                        #if elm is gt smallest target then it is correct since this is SHORT
                        if transformed_elm >= float(comparative_smallest_target):
                        #convert transformed element to string and replace elm
                            data[item][idx] = str(transformed_elm)
                        else:
                        #divide by 10 to shift 1dp to right and replace with str of elm
                            data[item][idx] = str(transformed_elm/10)
        print(data)
        return data
            






#divided_value = get_symbol_market_value_and_divide_by_two('1INCHUSDT')
#print(f"Market value of {symbol}: {float(market_value)}")
#print('divided_value',divided_value)

data_body = {'ticker': '1INCHUSDT', 'side': 'LONG', 'leverage': '20', 'entry': ['5400', '6200'], 'targets': ['6320', '6340', '6400', '6520', '6760'], 'stop': '4935'}

data_body_1 = {'ticker': '1INCHUSDT', 'side': 'LONG', 'leverage': '20', 'entry': ['940', '950'], 'targets': ['970', '990', '1020', '1040', '1070', '1100'], 'stop': '900'}

data_body_2 = {'ticker': 'AVAXUSDT', 'side': 'LONG', 'leverage': '20', 'entry': ['57', '54.5'], 'targets': ['59', '62', '63', '65', '66', '67', '70', '75'], 'stop': '50'}


#a function to get the number by which to divide the numbers in the data body
def get_divisor(market_value_div_by_2):
    
    # Count the number of decimal places in number
    decimal_places = len(str(market_value_div_by_2).split('.')[1])

    # Calculate the divisor
    divisor = 10 ** decimal_places

    return divisor

# divisor = get_divisor(divided_value)
# print('divisor', divisor)


# def update_data_ticker_value(data):
#     #divide number from data by divisor
#     divisor = get_divisor(divided_value)

#     #iterate over the data items
#     for item in ['entry', 'targets', 'stop']:

#         iter_item  = data[item]
#         print(data[item])
#         #stop is not an array, sort it out first
#         if item == 'stop':
#             #print('stop_item', iter_item)
#             data[item] = str(float(data[item])/divisor)
#             #print('stop_itemaf', iter_item)
#             #print(data)
#         else:
#             data[item] = [str(float(x)/divisor) for x in data[item]]

#     print(data)

#number_to_trade = modify_extracted_data_body(data_body)
#print('number to trade', number_to_trade)
