from test2 import sentinel_data_get_from_file
from utilities import check_lines_with_numbers



# Example usage
input_text = """
2024-02-19 15:00:08+00:00
Binance Futures, ByBit USDT, KuCoin Futures
#TOKEN/USDT Take-Profit target 2 ✅
Profit: 33.8983% 📈
Period: 2 Hours 0 Minutes ⏰
"""

result = check_lines_with_numbers(input_text)
#print(result)  # Output: True

def extract_blocks(file_path):
    # Initialize an empty list to store the blocks of text
    blocks = []
    sep = '='*30

    # Open the file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the entire content of the file
        file_content = file.read()

        # Split the content into blocks using '==' as the delimiter
        block_list = file_content.split(sep)

        # Iterate through each block and add it to the blocks list
        for block in block_list:
            # Remove leading and trailing whitespace characters
            cleaned_block = block.strip()
            # Skip empty blocks
            if cleaned_block:
                #print(cleaned_block)
                data_block = check_lines_with_numbers(cleaned_block)
                #print(data_block)
                if data_block:
                    #print(data_block)
                    blocks.append(data_block)

    return blocks

# Example usage
file_path = 'sentinel.txt'  # Replace 'example.txt' with your file path
blocks = extract_blocks(file_path)
print(len(blocks))
sep1 = '-'*30
sep2 = '='*30
count = 0
# Print each extracted block
for idx, block in enumerate(blocks, start=1): #get the last 100 (blocks[-100:])
    #call sentinel_data_get_from_file in order to create a json object from block (of text)
    json_block = sentinel_data_get_from_file(block)
    #if block length is not 6(there are supposed to be 6 items in the dict)
    if len(json_block) != 6:
         continue
    else:
        try:
            with open('jsonblocx.txt', 'a',  encoding='utf-8') as file:  # Open file in append mode
                    for line in block.splitlines():
                        file.write(f'{line}\n')
                    file.write(f'{sep1}\n')
                    file.write(f'{json_block}\n')
                    file.write(f'{sep2}\n')
                    count += 1
            first_entry_item = json_block['entry'][0]
            #filter out data with entry value >1 so as to test data_modify on them
            if float(first_entry_item) > 1 and not '.' in first_entry_item:
                 with open('jsonproblem.txt', 'a',  encoding='utf-8') as file: # a file to write the problem files
                      file.write(f'{json_block}\n')
                      file.write(f'{sep2}\n')
        except AttributeError:
                continue
print(count)


