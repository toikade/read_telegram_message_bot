# Define the numbers
number1 = 6352
number2 = 0.3111

# Count the number of decimal places in number2
decimal_places = len(str(number2).split('.')[1])

# Calculate the divisor
divisor = 10 ** decimal_places

# Divide number1 by the divisor
result = number1 / divisor

print("Divisor:", divisor)
print("Result:", result)
