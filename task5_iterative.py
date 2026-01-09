# Iterative approach using a loop
# This method calculates factorial by repeatedly multiplying values

import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task5 iterative.py <non-negative integer>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if n < 0:
            raise ValueError
    except ValueError:
        print("Please provide a valid non-negative integer.")
        sys.exit(1)

    result = 1
    for i in range(2, n + 1):
        result *= i

    print(result)
