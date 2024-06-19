from utilities import filter_text_with_numbers
from data_extract_functions import extract_signal_data_from_harrisons

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
                data_block = filter_text_with_numbers(cleaned_block)
                #print(data_block)
                if data_block:
                    #print(data_block)
                    blocks.append(data_block)

    return blocks

# Example usage
file_path = 'harrisonfutures.txt'  # Replace 'example.txt' with your file path
blocks = extract_blocks(file_path)
for block in blocks:
    print(block)
    print('='*30)
print(len(blocks))
sep1 = '-'*30
sep2 = '='*30
count = 0
# Print each extracted block
for idx, block in enumerate(blocks): #start at 1st block(blocks, start=1) #get the last 100 (blocks[-100:])
    #call sentinel_data_get_from_file in order to create a json object from block (of text)
    print(block)
    json_block = extract_signal_data_from_harrisons(block)
    #if block length is not 6(there are supposed to be 6 items in the dict)
    # if len(json_block) != 6:
    #      print(json_block)
    #      continue
    #else:
    try:
            with open('jsonblocx.txt', 'a',  encoding='utf-8') as file:  # Open file in append mode
                    for line in block.splitlines():
                        file.write(f'{line}\n')
                    file.write(f'{sep1}\n')
                    file.write(f'{json_block}\n')
                    file.write(f'{sep2}\n')
                    count += 1
    except TypeError as e:
        print('Error', e)
        continue