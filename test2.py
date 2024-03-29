import re
from utilities import get_next_line_items, get_number_from_str

test_str = """
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



    
def check_text_line_in_block(text):
    lines = text.splitlines()
    print(lines)
    for line in lines:
        if 'Leverage' in line:
            print(True)
            return line
            

#print(check_text_line_in_block(test_str))
        
