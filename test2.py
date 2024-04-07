import re
#from utilities import get_next_line_items, get_number_from_str

test_str = """
⚡️⚡️ #ADA/USDT ⚡️⚡️
Exchanges: Binance Futures
Signal Type: Regular (Long)
Leverage: Cross (75х)

Entry Targets: 0.7875

Take-Profit Targets:
1)0.7993
2)0.8072
3)0.8151
4)0.8269
5)0.8347
6)0.8466
7) 🚀🚀🚀

Stop Targets: 5-10%

"""
test_str1 = """
#API3/USDT
LONG
Leverage 20x 

Entry
 3.3523
3.2563
p
Targets
3.38582
3.41935
3.45287
3.55344

SL
3.017
"""
def check_lines_with_numbers(text):
    lines = text.splitlines()
    count = 0
    print(lines)
    
    for line in lines:
        # Check if the line contains a number (integer or decimal)
        if any(char.isdigit() or char == '.' for char in line):
            count += 1
    
    if count >= 6:  # Return True if there are 6 or more lines with a number
        return text
    else:
        return 0
    

#print(check_lines_with_numbers(test_str))
    


#print(get_next_line_items(test_str))

def sentinel_data_get_from_file(text):
    tradeData = {}
    error_counter = 0
    try:
        ticker = re.findall(r'\#\w+', text)    #get ticker
        ticker = str(ticker[0][1:]+'USDT')
        print(ticker)
        tradeData['ticker'] = ticker    #add ticker to dict
        lines = text.splitlines()       #split lines wrt to \n
        #lines = [i for i in lines if i != '']   # filter to remove empty items
    
        #print(lines)
        entry_and_target = get_next_line_items(lines)

        tradeData['side'] = [i for i in lines if i.lower()=='long' or i.lower()=='short'][0]
        tradeData['leverage'] = [get_number_from_str(line) for line in lines if 'Leverage' in line][0]
        tradeData['entry'] = entry_and_target[0]
        tradeData['targets'] = entry_and_target[1]
        tradeData['stop'] = lines[-1]

    except:
        pass

    return tradeData

#print(sentinel_data_get_from_file(test_str))

#get_number_from_str eg ('Leverage 20x')    
def get_number_from_str(text):
    num = ''
  
    for i in text:
            if i.isdigit():
                num += i   
    return num

#get the change value from a percentage
def get_value_change_amount_from_percentage(percentage, entryValue):
    entryValue = float(entryValue)
    decreaseAmount = entryValue*(percentage/100)
    afterDecreaseValue = entryValue - decreaseAmount
    return afterDecreaseValue

#a fxn to scrape data from harrison's tradingchannel and make it a dict
def harrison_get_from_file(text):
    tradeData = {}
    error_counter = 0
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        #if line: #remove any empty lines
        print(line)
        try:
                #extract char from the line is alphabetic and 'USDT' is also in line then use str method to join
                if 'USDT' in line:
                    ticker = ''.join([i for i in line if i.isalpha() is True])    #get ticker
                    #ticker = str(ticker[0][1:]+'USDT')
                    print(ticker)
                    tradeData['ticker'] = ticker
                    #break
                elif 'long' in line.lower():
                    tradeData['side'] = 'LONG'
                elif 'short' in line.lower():
                    tradeData['side'] = 'SHORT'
                elif 'leverage' in line.lower():
                    tradeData['leverage'] = get_number_from_str(line)
                elif 'entry' in line.lower():
                    entry_data = [i for i in line.split() if i[0].isdigit()]
                    if entry_data:
                            tradeData['entry'] = entry_data
                    else:
                            collected_items = []
                            start_index = idx
                            while (lines[start_index+1]):
                                #strip line to handle lines with a leading whitespace
                                second_condition = lines[start_index+1].strip()[0].isdigit() 
                                print('LINE', line, idx, start_index)
                                if not second_condition:    # if line is not a digit
                                    break
                                else:
                                    #if there is more than 1 item per line and no empty item
                                    if len(lines[start_index+1].split(' ')) > 1 and '' not in lines[start_index+1].split(' '):
                                        for item in lines[start_index+1].split(' '):
                                            match = re.search(r"\d+\.\d+|\d+", item)
                                            number = match.group()
                                            collected_items.append(number)
                                    else:
                                        
                                        collected_items.append(lines[start_index+1].strip())
                                #increase the index for while loop iteration  
                                start_index += 1
                            tradeData['entry'] = collected_items
                            continue 
                #if profit or tp in the line
                elif 'profit' in line.lower() or 'tp' in line.lower():
                    start_index = idx
                    collected_items =[]
                    print('HERE', line, start_index)
                    #while the next line is a valid line
                    while(lines[start_index+1]):
                        #seperators that can be found in the lines
                        sep = [i for i in lines[start_index+1] if not i.isalpha() and not i.isdigit()]
                        print(sep)
                        #if after the split there are not 2 items i.e no seperator and the 1st sep is not '.'
                        if not len(lines[start_index+1].split()) > 1 and sep[0] != '.':
                            print('ln', line)
                            #use the first seperator from the list of seperators to seperate it
                            splitline = lines[start_index+1].split(sep[0])
                        else:
                            # split the line with a space
                            splitline = lines[start_index+1].split()
                        #if second item of splitline splitline[1][0] is a digit then consider it
                        if splitline[1][0].isdigit():
                            #add it to collected items array
                            collected_items.append(splitline[1])
                        start_index +=1
                    tradeData['targets'] = collected_items
                # get the STOP LOSS
                elif 'loss' in line.lower() or 'sl' in line.lower() or 'stop' in line.lower():
                    #if title and data on the same line and items gt 2 and a digit on 2nd item
                    if len(line.split()) > 1 and line.split()[-1][0].isdigit():
                        #take the last value on the line
                        stopValue = line.split()[-1].strip()
                        
                        if '%' not in stopValue:
                            #no %, take the value as it is
                            tradeData['stop'] = stopValue
                        else:
                            #get the gt value from array to be stop % given there is a %
                            stopValue = max([int(get_number_from_str(i)) for i in stopValue.split('-')]) #remove max to get both values
                            print('stp',stopValue)
                            stopValue = get_value_change_amount_from_percentage(stopValue, tradeData['entry'][0])
                            tradeData['stop'] = str(stopValue)
                            print('perc', stopValue)
                       
                    else:
                        #get value from next line
                        stopValue = lines[idx+1]
                        if '%' not in stopValue:
                            #no %, take the value as it is
                            tradeData['stop'] = stopValue
                        else:
                            #get the gt value from array to be %
                            stopValue = max([int(get_number_from_str(i)) for i in stopValue.split('-')])
                            stopValue = get_value_change_amount_from_percentage(stopValue, tradeData['entry'][0])
                            tradeData['stop'] = str(stopValue)
                            #print('stp',stopValue)
                else:
                    continue

        except Exception as e:
            print(e)    
    return tradeData
    

print(harrison_get_from_file(test_str))
    
def check_text_line_in_block(text):
    lines = text.splitlines()
    print(lines)
    for line in lines:
        if 'Leverage' in line:
            print(True)
            return line
            

#print(check_text_line_in_block(test_str))
        
