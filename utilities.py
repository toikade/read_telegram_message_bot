from decouple import config
from binance.client import Client
import re, unicodedata, ftfy
from unidecode import unidecode

# Initialize Binance client
# api_key = config('BINANCE_FUTURES_DEMO_API_KEY', cast=str)
# api_secret = config('BINANCE_FUTURES_DEMO_SECRET', cast=str)
# client = Client(api_key, api_secret, testnet=True)

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

# a function to get info about an asset such as precisions for price and quantity
def get_asset_precision(symbol):
    try:
        # Get exchange information
        exchange_info = client.futures_exchange_info()

        # Find the symbol details
        for symbol_info in exchange_info['symbols']:
            if symbol_info['symbol'] == symbol:
                #return symbol_info['filters'][0]['tickSize']
                #print('ticksize',symbol_info['filters'][0]['tickSize'])
                #print('priceprecision',symbol_info['pricePrecision'])
                #print('quantityprecision',symbol_info['quantityPrecision'])
                #print(symbol_info)
                return symbol_info

        print(f"Symbol {symbol} not found.")
        return symbol_info

    except Exception as e:
        print(f"Error: {e}")
        return None

# a function to transform a number by padding it with leading zeroes
def transform_number(number, leading_zeros_count):
    # start with a number e.g  '123'
    number = str(number)
    #if there is no leading_zero
    if leading_zeros_count == 0:
        #add just 1 zero before the number
        transformed_number = '0' + '.' + number
    else:
        #add zero and the number of leading zeros
        transformed_number = '0' + '.' + ('0'*leading_zeros_count) + number
    return transformed_number

# a function to set price with asset precision
def set_asset_precision(price_precision, num):
    price_precision = price_precision
    num_str = str(float(num))
    #number of dp after the .
    dp_length = len(num_str.split('.')[1])
    #if number of dp lt price_precision
    if dp_length < price_precision:
        #calculate how places are left to fill
        places_to_fill_number = price_precision - dp_length
        #fill the spaces with zeroes
        num_str = num_str + '0'*places_to_fill_number
    #if number of dp is gt price_precision
    elif dp_length > price_precision:
        #a variable to hold index for dot
        dot_index = 0
        #iterate inorder to get index of . from which to start counting
        for idx, i in enumerate(num_str):
            #if you find the dot
            if i == '.':
                dot_index = idx
                break
            #calculate the number of decimals to consider and truncate
        dp_number_to_consider = dot_index + price_precision
        num_str = num_str[:dp_number_to_consider]
    #if the number respects the price precision
    else:
        pass
    return num_str


#a function to calculate asset precision
# def calc_asset_precision(data):
#     price_precision = get_asset_precision(data['ticker'])['pricePrecision']
#     for item in ['entry', 'targets']:
#         data[item] = [set_asset_precision(price_precision, i) for i in data[item]] 
#     data['stop'] = set_asset_precision(price_precision, data['stop'])
#     return data

#a function to determine the number of leading zeros in a decimal number
def leading_zero_counter(number):
    # start with str of number e.g '0.00123'
    strin = str(number)
    dot_index = 0
    zero_count = 0
    #iterate through number
    for idx, i in enumerate(strin):
        #if you meet dot
        if strin[idx] == '.':
            #get the index of dot
            dot_index = idx
        #if you continue and index is gt index of dot
        if idx > dot_index:
            #if the char(i) is ne 0 means there is no more leading 0
            if i != '0':
                break
            #else if you find a 0 increase zero_counter by 1
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
        

def filter_text_with_numbers(text):
    lines_with_numbers = 0
    for line in text.split('\n'):
        # Check if the line contains numbers (or decimals)
        # Drop line if tronscan.org in it
        word_list = ['tronscan','bln', 'cornix', 'top 5', 'trending', 'booking', 'liquidated', 'cup & handle', 'dead cat','accumulating', 'capitalization','accumulation','double bottom', 'three white soldiers']
        for word in word_list:
            if  word in line.lower():
                return False
        if(len(line)>=100):
            return False
        if any(char.isdigit() or char == '.' for char in line):
            lines_with_numbers += 1
            if lines_with_numbers >= 6:
                return text  # Filter out the text if there are numbers on at least six lines
    return False
        
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


def block_contains_usd_or_usdt(text):
    # Check each line for 'USD' or 'USDT' (case insensitive)
    for idx, line in enumerate(text.splitlines()):
        #Get USD or USDT as a block(good for SUSHI/USDT and #DUSK/USDT cases)
        if re.search(r'(usdt|usd)', line, re.IGNORECASE):
            return line
    
        elif idx<5:
            symbols = get_binance_futures_asset_list_from_file()
            for symbol in symbols:
                if symbol in line:
                    return symbol+'USDT'
    return None

#get the change value from a percentage
def get_value_change_amount_from_percentage(percentage, entryValue, side):
    entryValue = float(entryValue)
    percentage = float(percentage)
    changeAmount = entryValue*(percentage/100)
    try:
        if side == 'LONG':
            afterDecreaseValue = entryValue - changeAmount
        else:
            afterDecreaseValue = entryValue + changeAmount
        return str(round(afterDecreaseValue, 4) #round the number to 4dp and convert to str
    except KeyError as ke:
        print(ke)

#extract the ticker from harrisons data block
def extract_ticker_from_harrisons_data_block(text):
    line = block_contains_usd_or_usdt(text)
    line_without_usd = re.sub(r'(usdt|usd)', '', line, flags=re.IGNORECASE)
    # Extract all alphanumeric characters from the remaining line
    alphanumeric_chars = re.findall(r'[A-Za-z0-9]+', line_without_usd)
   
    asset_string = ''.join(alphanumeric_chars)

    concatenated_string = asset_string + 'USDT'
    return concatenated_string

def extract_entry_values_from_harrisons_data_block(text):
    # Normalize text to convert confusing unicode chars to alphabet
    text = unicodedata.normalize('NFKD', text)
    # Split the text into lines
    lines = text.splitlines()
    results = []
    target_line_index = -1

    # Find the line containing 'entr' as part of any word
    for i, line in enumerate(lines):
        if re.search(r'\b.*entr.*\b', line, re.IGNORECASE):
            target_line_index = i
            # Extract numbers from the line with 'entr'
            numbers = re.findall(r'\b\d+(?:\.\d+)?\b', line)
            if numbers:
                results.extend(numbers)
                break
    
    # If no numbers are found on the 'entr' line, check the following two non-blank lines
    if not results and target_line_index != -1:
        non_blank_line_count = 0
        for j in range(target_line_index + 1, len(lines)):
            if non_blank_line_count >= 2:
                break
            if lines[j].strip():  # Check if the line is not blank
                non_blank_line_count += 1
                # Extract numbers ignoring enumerations like '1)' or '1-'
                numbers = re.findall(r'\b\d+(?:\.\d+)?\b', re.sub(r'^\s*\d+[\)\-]\s*', '', lines[j]))
                if numbers:
                    results.extend(numbers)
                if len(results) >= 2:
                    break

    # If still no numbers are found, search for 'buy' line
    if not results:
        for line in lines:
            if re.search(r'buy', line, re.IGNORECASE):
                # Extract numbers from the line with 'buy'
                numbers = re.findall(r'\b\d+(?:\.\d+)?\b', line)
                if numbers:
                    results.extend(numbers)
                if len(results) >= 2:
                    break

    # If no numbers are found, return 'market'
    if not results:
        return 'market'

    # Return up to two groups of numbers
    return results[:2]

def extract_target_values_from_harrisons_data_block(text):
    # Define the pattern to match numbering formats
    numbering_pattern = re.compile(r'^\s*(?:\d+\)|\d+-|target\s+\d+\s*-|target\s+\d+:|take-profit\s+\d+:|tp\s+\d+-)', flags=re.IGNORECASE)
    number_pattern = re.compile(r'\d+(?:\.\d+)?')
    ignore_pattern = re.compile(r'(entr|lever)', flags=re.IGNORECASE)

    def get_numbers_from_lines(lines, min_consecutive):
        numbers = []
        consecutive_lines = []
        consecutive_count = 0
        
        for line in lines:
            # Skip lines containing 'entr' or 'lever'
            if re.search(ignore_pattern, line):
                continue
            
            # Strip '*' characters from the line
            line = line.replace('*', '')
            
            # Remove numbering from the line
            line_without_numbering = re.sub(numbering_pattern, '', line)
            
            # Extract numbers from the line
            matches = re.findall(number_pattern, re.sub(r'\([^)]*\)', '', line_without_numbering))
            
            if matches:
                consecutive_lines.append(line)
                numbers.extend(matches)
                consecutive_count += 1
            else:
                # Reset if fewer than required consecutive lines with numbers are found
                if consecutive_count >= min_consecutive:
                    break
                numbers = []
                consecutive_lines = []
                consecutive_count = 0
        
        return numbers if consecutive_count >= min_consecutive else []

    # Split the text into lines
    lines = text.splitlines()
    
    # Try to get numbers from at least 3 consecutive lines first
    numbers = get_numbers_from_lines(lines, 3)
    
    if not numbers:
        # Try to get numbers from at least 2 consecutive lines as a fallback
        numbers = get_numbers_from_lines(lines, 2)
    
    return numbers

#extract leverage value from harrisons data block
def extract_leverage_value_from_harrisons_data_block(text):
    specific_replacements = {
    '\u0445': 'x',  # Cyrillic 'х' to Latin 'x'
    # Add more specific replacements if needed
    }
    
    def normalize_text(text):
        #normalize text to remove characters that resemble alphabet but are not
        text = unicodedata.normalize('NFKD', text)
        # Use ftfy to fix text encoding issues
        text = ftfy.fix_text(text)
        for char, replacement in specific_replacements.items():
            text = text.replace(char, replacement)
        # Use unidecode for broader transliteration
        text = unidecode(text)
        return text

    text = normalize_text(text)
    # Split the text into lines
    lines = text.split('\n')
    
    # Compile the regex pattern to match one or more digits followed by 'x' (case insensitive)
    pattern = re.compile(r'(\d+(\.\d+)?)x', re.IGNORECASE)
    
    # List to store the smallest matching number per line
    smallest_matching_numbers = []
    
    matches = pattern.findall(text)

    # Extract only the integer parts of the numbers from the matches
    numbers = [str(int(float(match[0]))) for match in matches]
    #if numbers is empty i.e no value found to return, return 1
    if not len(numbers): #empty array
        numbers.append('1')
    else:
        numbers = [str(min(map(int, numbers)))]
    return numbers

#extract the stoploss value from harrisons data block
def extract_stop_value_from_harrisons_data_block(text):
    #normalize text against characters that resemble alphabet but are not
    text = unicodedata.normalize('NFKD', text)
   # Split the text into lines
    lines = text.split('\n')
    
    # Compile regex pattern for relevant keywords
    keywords_pattern = re.compile(r'(?i)(stop|stolen|SL[\s\W])')
    
    # Store relevant lines
    relevant_lines = []
    relevant_line_idx = 1000000 #initiate holder for relevant_line index when it is found
    stoploss_words = ['DCA', 'HOLD']

    for idx, line in enumerate(lines):
        if keywords_pattern.search(line): # Check if the line has relevant word
            if re.search(r'\d', line): #is there a number on the relevant line
                relevant_lines.append(line)
            elif 'hold' in line.lower() or 'dca' in line.lower(): #if stop loss says HOLD and DCA
                relevant_lines.append('10%') #return 10 for a default of 10%
            else: #found nothing on the relevant line
                relevant_line_idx = idx
        if (idx > relevant_line_idx) and re.search(r'\d', line): #if index >relevant line idx and a number on that line
            relevant_lines.append(line)
            break

     # Process the relevant lines
    processed_lines = []
    for line in relevant_lines:
        # Ignore brackets and their contents
        line = re.sub(r'\([^)]*\)', '', line)
        
        # Ignore line numbering like "1)"
        line = re.sub(r'^\d+\)\s*', '', line)
        
        # Check if '%' is in the line
        if '%' in line:
            match = re.search(r'(\d+(\.\d+)?)\s*%', line)
            if match:
                # Check if there is a decimal point
                number = match.group(1)
                if '.' in number:
                    # Get the part after the decimal point e.g 5.10
                    decimal_part = number.split('.')[1]
                    processed_lines.append(decimal_part + '%')
                else:
                    processed_lines.append(number + '%')
        elif '5-10' in line:
            processed_lines.append('10%')
        else:
            # Find the first group of numbers
            match = re.search(r'(\d+(\.\d+)?)', line)
            if match:
                processed_lines.append(match.group(1))
    
    return processed_lines  

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

data_body_3 = {'ticker': '1INCHUSDT', 'side': 'LONG', 'leverage': '20', 'entry': ['0.540', '0.62'], 'targets': ['0.632', '0.6340', '0.640', '0.652', '0.676'], 'stop': '0.4935'}

#print(calc_asset_precision(data_body_3))

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
def get_binance_futures_asset_list():
    exchange_info = client.futures_exchange_info()
    # Extract all symbols ending with 'USDT' or 'USDC'
    symbols_usdt_usdc = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['symbol'].endswith(('USDT', 'USDC'))]

    # Strip away 'USDT' or 'USDC' from the symbols
    stripped_symbols = [symbol.replace('USDT', '').replace('USDC', '') for symbol in symbols_usdt_usdc]

    return stripped_symbols
    
# with open('binance_futures_asset_list.txt', 'a',  encoding='utf-8') as file:
#     for i in binance_futures_asset_list():
#         if i != '':
#             file.write(f'{i}\n')

def get_binance_futures_asset_list_from_file():
    with open('binance_futures_asset_list.txt', 'r', encoding='utf-8') as file:
        # Read the entire content of the file
        file_content = file.read()

        # Split the content into blocks using '==' as the delimiter
        asset_list = file_content.split('\n')
        #remove trailing empty element
        del asset_list[len(asset_list)-1]
        return asset_list
    
#print(get_binance_futures_asset_list_from_file())
# with open('harrisonfutures.txt', 'r', encoding='utf-8') as file:
#     # Read the entire content of the file
#     file_content = file.read()
#     lines = file_content.splitlines()
#     for line in lines:
#         if 'Cornix' in line:
#             print(line)
#             print('+'*30)
