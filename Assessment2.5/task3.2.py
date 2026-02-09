# Write a Python function to reverse an integer with 32-bit signed integer overflow handling.

def reverse_integer(x):
    """
    Reverse an integer with 32-bit signed integer overflow handling.
    
    Args:
        x: An integer to reverse
        
    Returns:
        The reversed integer, or 0 if the reversed integer overflows 32-bit signed integer range
        (i.e., outside [-2^31, 2^31 - 1] = [-2147483648, 2147483647])
    """
    # Handle negative numbers
    is_negative = x < 0
    num = abs(x)
    
    # Reverse the digits
    reversed_num = 0
    while num > 0:
        reversed_num = reversed_num * 10 + num % 10
        num //= 10
    
    # Apply sign
    if is_negative:
        reversed_num = -reversed_num
    
    # Check for 32-bit signed integer overflow
    INT_MIN = -2**31  # -2147483648
    INT_MAX = 2**31 - 1  # 2147483647
    
    if reversed_num < INT_MIN or reversed_num > INT_MAX:
        return 0
    
    return reversed_num


# Test cases
if __name__ == "__main__":
    # Test case 1: Positive number
    print(f"reverse_integer(123) = {reverse_integer(123)}")  # Expected: 321
    
    # Test case 2: Negative number
    print(f"reverse_integer(-123) = {reverse_integer(-123)}")  # Expected: -321
    
    # Test case 3: Number ending with zero
    print(f"reverse_integer(120) = {reverse_integer(120)}")  # Expected: 21
    
    # Test case 4: Single digit
    print(f"reverse_integer(5) = {reverse_integer(5)}")  # Expected: 5
    
    # Test case 5: Zero
    print(f"reverse_integer(0) = {reverse_integer(0)}")  # Expected: 0
    
    # Test case 6: Overflow case (reversed number exceeds INT_MAX)
    print(f"reverse_integer(1534236469) = {reverse_integer(1534236469)}")  # Expected: 0 (overflows)
    
    # Test case 7: Overflow case (reversed number exceeds INT_MIN)
    print(f"reverse_integer(-2147483648) = {reverse_integer(-2147483648)}")  # Expected: 0 (overflows)