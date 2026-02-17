# Write a Python function that accepts a list of integers and returns the count of all positive numbers in the list. Do not use any example input while generating the logic. Also test the function with a sample input.

def count_positive_numbers(int_list):
    count = 0
    for num in int_list:
        if num > 0:
            count += 1
    return count  
# Testing the function with a sample input
sample_input = [1, -2, 3, 4, -5, 0]
result = count_positive_numbers(sample_input)
print(result)  # Output: 3



