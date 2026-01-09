# In Task 2, the AI-generated code from Task 1 was reviewed and optimized.
import sys
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task2.py <non-negative integer>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if n < 0:
            raise ValueError
    except ValueError:
        print("Please provide a valid non-negative integer.")
        sys.exit(1)

    product = 1
    for i in range(2, n + 1):
        product *= i

    print(product)