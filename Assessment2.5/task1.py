# Task 1: Refactoring Odd/Even Logic (List Version)
# ❖ Scenario:
# You are improving legacy code.
# ❖ Task:
# Write a program to calculate the sum of odd and even numbers in a list,
# then refactor it using AI.
# ❖ Expected Output:
# ❖ Original and improved code

# Original Code (Legacy Style)
def calculate_sums_original(numbers):
    odd_sum = 0
    even_sum = 0
    i = 0
    while i < len(numbers):
        if numbers[i] % 2 == 0:
            even_sum = even_sum + numbers[i]
        else:
            odd_sum = odd_sum + numbers[i]
        i = i + 1
    return odd_sum, even_sum

# Test the original code
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
odd, even = calculate_sums_original(numbers)
print(f"Original Code:")
print(f"Sum of odd numbers: {odd}")
print(f"Sum of even numbers: {even}")