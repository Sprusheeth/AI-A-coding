# Recursive approach using function calls
# The function calls itself until it reaches the base case

import sys

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task5_recursive.py <non-negative integer>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if n < 0:
            raise ValueError
    except ValueError:
        print("Please provide a valid non-negative integer.")
        sys.exit(1)

    print(factorial(n))
