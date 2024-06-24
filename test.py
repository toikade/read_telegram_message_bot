#from test2 import sentinel_data_get_from_file
#from utilities import check_lines_with_numbers
from utilities import block_contains_usd_or_usdt
import re
import unicodedata


# Example usage
input_text = """
2024-02-19 15:00:08+00:00
Binance Futures, ByBit USDT, KuCoin Futures
#TOKEN/USDT Take-Profit target 2 ✅
Profit: 33.8983% 📈
Period: 2 Hours 0 Minutes ⏰
"""

# result = check_lines_with_numbers(input_text)
# #print(result)  # Output: True

# def extract_blocks(file_path):
#     # Initialize an empty list to store the blocks of text
#     blocks = []
#     sep = '='*30

#     # Open the file in read mode
#     with open(file_path, 'r', encoding='utf-8') as file:
#         # Read the entire content of the file
#         file_content = file.read()

#         # Split the content into blocks using '==' as the delimiter
#         block_list = file_content.split(sep)

#         # Iterate through each block and add it to the blocks list
#         for block in block_list:
#             # Remove leading and trailing whitespace characters
#             cleaned_block = block.strip()
#             # Skip empty blocks
#             if cleaned_block:
#                 #print(cleaned_block)
#                 data_block = check_lines_with_numbers(cleaned_block)
#                 #print(data_block)
#                 if data_block:
#                     #print(data_block)
#                     blocks.append(data_block)

#     return blocks

# # Example usage
# file_path = 'sentinel.txt'  # Replace 'example.txt' with your file path
# blocks = extract_blocks(file_path)
# print(len(blocks))
# sep1 = '-'*30
# sep2 = '='*30
# count = 0
# # Print each extracted block
# for idx, block in enumerate(blocks, start=1): #get the last 100 (blocks[-100:])
#     #call sentinel_data_get_from_file in order to create a json object from block (of text)
#     json_block = sentinel_data_get_from_file(block)
#     #if block length is not 6(there are supposed to be 6 items in the dict)
#     if len(json_block) != 6:
#          continue
#     else:
#         try:
#             with open('jsonblocx.txt', 'a',  encoding='utf-8') as file:  # Open file in append mode
#                     for line in block.splitlines():
#                         file.write(f'{line}\n')
#                     file.write(f'{sep1}\n')
#                     file.write(f'{json_block}\n')
#                     file.write(f'{sep2}\n')
#                     count += 1
#             first_entry_item = json_block['entry'][0]
#             #filter out data with entry value >1 so as to test data_modify on them
#             if float(first_entry_item) > 1 and not '.' in first_entry_item:
#                  with open('jsonproblem.txt', 'a',  encoding='utf-8') as file: # a file to write the problem files
#                       file.write(f'{json_block}\n')
#                       file.write(f'{sep2}\n')
#         except AttributeError:
#                 continue
# print(count)


# def extract_numbers_after_targ(text):
#     # Split the text into lines
#     lines = text.splitlines()
#     results = []
#     target_line_index = -1

#     # Find the line containing 'targ' without 'entr' or 'buy' and no numbers on the same line
#     for i, line in enumerate(lines):
#         if re.search(r'targ', line, re.IGNORECASE) and not re.search(r'entr|buy', line, re.IGNORECASE) and not re.search(r'\d', line):
#             target_line_index = i
#             break

#     # If a target line is found, process subsequent lines to extract numbers
#     if target_line_index != -1:
#         found_numbers = False
#         for j in range(target_line_index + 1, len(lines)):
#             if lines[j].strip() == '':  # Skip blank lines after 'targ'
#                 if found_numbers:  # Stop if a blank line is found after numbers
#                     break
#                 continue
#             # Extract numbers ignoring enumerations like '1)', '1 -', or 'target 1'
#             # We only consider the first group of numbers found on the same line
#             match = re.search(r'\b\d+(?:\.\d+)?(?!\%)\b', re.sub(r'^\s*(\d+[\)\-]\s*|target\s*\d+\s*)', '', lines[j], flags=re.IGNORECASE))
#             if match:
#                 # Get the first group of numbers found on the line
#                 first_number = match.group(0)
#                 # Strip any leading or trailing non-alphanumeric characters from the number
#                 cleaned_number = re.sub(r'^\W+|\W+$', '', first_number)
#                 results.append(cleaned_number)
#                 found_numbers = True

#     return results

def process_lines(text):
    #mormalize text to remove characters that resemble alphabet but are not
    text = unicodedata.normalize('NFKD', text)
    # Split the text into lines
    lines = text.split('\n')
    
    # Compile the regex pattern to match one or more digits followed by 'x' (case insensitive)
    pattern = re.compile(r'(\d+)x', re.IGNORECASE)
    
    # List to store the smallest matching number per line
    smallest_matching_numbers = []
    
    # Iterate over each line and check for the pattern
    for idx, line in enumerate(lines):
        matches = pattern.findall(line)
        if matches:
            # Convert matches to integers and find the smallest one
            smallest_number = min(map(int, matches))
            smallest_matching_numbers.append(smallest_number)
            break
        if idx >=len(lines)-1:
            smallest_matching_numbers.append('1')
    
    return smallest_matching_numbers


# def extract_numbers(text):
#     # Split the text into lines
#     text = unicodedata.normalize('NFKD', text)
#     lines = text.splitlines()
#     results = []
#     target_line_index = -1

#     # Find the line containing 'entr' as part of any word
#     for i, line in enumerate(lines):
#         if re.search(r'\b.*entr.*\b', line, re.IGNORECASE):
#             target_line_index = i
#             # Extract numbers from the line with 'entr'
#             numbers = re.findall(r'\b\d+(?:\.\d+)?\b', line)
#             if numbers:
#                 results.extend(numbers)
#                 break
    
#     # If no numbers are found on the 'entr' line, check the following two non-blank lines
#     if not results and target_line_index != -1:
#         non_blank_line_count = 0
#         for j in range(target_line_index + 1, len(lines)):
#             if non_blank_line_count >= 2:
#                 break
#             if lines[j].strip():  # Check if the line is not blank
#                 non_blank_line_count += 1
#                 # Extract numbers ignoring enumerations like '1)' or '1-'
#                 numbers = re.findall(r'\b\d+(?:\.\d+)?\b', re.sub(r'^\s*\d+[\)\-]\s*', '', lines[j]))
#                 if numbers:
#                     results.extend(numbers)
#                 if len(results) >= 2:
#                     break

#     # Return up to two groups of numbers
#     return results[:2]

# def extract_numbers(text):
#     # Split the text into lines
#     lines = text.splitlines()
#     results = []

#     # Find the line containing 'entr' as part of any word
#     for line in lines:
#         if re.search(r'\b.*entr.*\b', line, re.IGNORECASE):
#             # Extract numbers separated by spaces or non-alphanumeric characters (excluding dots)
#             numbers = re.findall(r'\b\d+(?:\.\d+)?\b', line)
#             results.extend(numbers)
#             # Stop after finding the first 'entr' line
#             break
    
#     # Return up to two groups of numbers
#     return results[:2]

# def filter_text(text):
#     line = block_contains_usd_or_usdt(text)
#     line = line.split('/')
#     print(line)
    # line_without_usd = re.sub(r'usdt?|usd?', '', line, flags=re.IGNORECASE)
    # print('WOUT', line_without_usd)
    # # Extract all alphanumeric characters from the remaining line
    # alphanumeric_chars = re.findall(r'[A-Za-z0-9]+', line_without_usd)
    # print('ALPNUM', alphanumeric_chars)
    # # Concatenate them together and append 'USDT'
    # concatenated_string = ''.join(alphanumeric_chars) + 'USDT'
    # ticker =  concatenated_string
    # #tradeData['ticker'] = ticker
    # print(ticker)
    # return None


# Example usage
text = """
⚡️⚡️#EOS/USDT⚡️⚡️

Signal Type: Short
Leverage: Cross 75X_25X

Entry Range: 0.8960

Take-Profit Targets:
1) 0.88256
2) 0.87360
3) 0.86464
4) 0.85120
5) 0.84224
6) 0.82880

Stoploss: 
5-10%
"""
result = process_lines(text)
print(result)  