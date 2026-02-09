# Write an optimized Python solution for reversing an integer with strict overflow checks for coding interviews.

def reverse_integer(x):
    """
    Optimized solution to reverse an integer with strict 32-bit signed integer overflow handling.
    
    Time Complexity: O(log10(n)) - where n is the input number
    Space Complexity: O(1) - constant extra space
    
    Args:
        x: An integer to reverse
        
    Returns:
        The reversed integer, or 0 if the reversed integer overflows 32-bit signed integer range
        (i.e., outside [-2^31, 2^31 - 1] = [-2147483648, 2147483647])
    """
    # 32-bit signed integer bounds
    INT_MIN = -2**31  # -2147483648
    INT_MAX = 2**31 - 1  # 2147483647
    
    result = 0
    
    while x != 0:
        # Extract the last digit
        digit = x % 10 if x > 0 else -(-x % 10)  # Handle negative modulo correctly
        x = x // 10 if x > 0 else -(-x // 10)  # Handle negative division correctly
        
        # Strict overflow check BEFORE multiplication
        # Check if result * 10 + digit would overflow
        
        # For positive overflow: result * 10 + digit > INT_MAX
        # Rearranged: result > (INT_MAX - digit) / 10
        if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > INT_MAX % 10):
            return 0
        
        # For negative overflow: result * 10 + digit < INT_MIN
        # Rearranged: result < (INT_MIN - digit) / 10
        if result < INT_MIN // 10 or (result == INT_MIN // 10 and digit < INT_MIN % 10):
            return 0
        
        # Safe to perform the operation
        result = result * 10 + digit
    
    return result


# Alternative optimized version (more Pythonic and cleaner)
def reverse_integer_v2(x):
    """
    Alternative optimized solution - cleaner approach handling sign separately.
    
    Time Complexity: O(log10(n))
    Space Complexity: O(1)
    """
    INT_MIN = -2**31
    INT_MAX = 2**31 - 1
    
    result = 0
    
    while x != 0:
        # Extract last digit (works for both positive and negative)
        digit = x % 10 if x >= 0 else x % -10
        x = x // 10 if x >= 0 else (x + 9) // 10  # Python's floor division for negatives
        
        # Check overflow before multiplication
        if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
            return 0
        if result < INT_MIN // 10 or (result == INT_MIN // 10 and digit < -8):
            return 0
        
        result = result * 10 + digit
    
    return result


# Most interview-friendly version (handles sign explicitly)
def reverse_integer_optimized(x):
    """
    Most optimized and interview-friendly version.
    Handles overflow checks during reversal for maximum efficiency.
    
    Key optimizations:
    1. Overflow check BEFORE multiplication (prevents unnecessary computation)
    2. Works with both positive and negative numbers
    3. O(log10(n)) time complexity - optimal for this problem
    4. O(1) space complexity - constant extra space
    
    Time Complexity: O(log10(n))
    Space Complexity: O(1)
    """
    INT_MIN = -2**31  # -2147483648
    INT_MAX = 2**31 - 1  # 2147483647
    
    result = 0
    
    while x != 0:
        # Extract last digit
        # Python's % operator returns non-negative remainder
        pop = x % 10
        x //= 10
        
        # Handle Python's negative modulo behavior
        # For negative numbers, we need to adjust
        if x < 0 and pop != 0:
            pop -= 10
            x += 1
        
        # Strict overflow check BEFORE multiplication
        # Check if result * 10 + pop would exceed INT_MAX
        if result > INT_MAX // 10 or (result == INT_MAX // 10 and pop > 7):
            return 0
        
        # Check if result * 10 + pop would be below INT_MIN
        if result < INT_MIN // 10 or (result == INT_MIN // 10 and pop < -8):
            return 0
        
        # Safe to perform the operation
        result = result * 10 + pop
    
    return result


# Test cases
if __name__ == "__main__":
    test_cases = [
        (123, 321),
        (-123, -321),
        (120, 21),
        (5, 5),
        (0, 0),
        (1534236469, 0),  # Overflow case
        (-2147483648, 0),  # Overflow case (INT_MIN)
        (2147483647, 0),   # Overflow case (INT_MAX reversed)
        (1463847412, 2147483641),  # Edge case - just within bounds
        (-1463847412, -2147483641),  # Edge case - just within bounds
    ]
    
    print("Testing reverse_integer_optimized:")
    print("-" * 60)
    for input_val, expected in test_cases:
        result = reverse_integer_optimized(input_val)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status:4} reverse_integer_optimized({input_val:12}) = {result:12} (expected: {expected:12})")
    
    print("\n" + "=" * 60)
    print("Performance comparison:")
    print("=" * 60)
    
    import time
    
    test_input = 123456789
    
    # Test reverse_integer_optimized
    start = time.perf_counter()
    for _ in range(1000000):
        reverse_integer_optimized(test_input)
    time1 = time.perf_counter() - start
    
    print(f"reverse_integer_optimized: {time1:.4f} seconds for 1M iterations")
