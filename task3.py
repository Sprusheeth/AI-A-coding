# Task 3: Modular Design Using AI Assistance (Factorial with Functions)
# The same logic now needs to be reused in multiple scripts.
import sys
def compute_factorial(n):
    if n < 0:
        raise ValueError("Negative values are not allowed.")
    product = 1
    for i in range(2, n + 1):
        product *= i
    return product
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task3.py <non-negative integer>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if n < 0:
            raise ValueError
    except ValueError:
        print("Please provide a valid non-negative integer.")
        sys.exit(1)

    result = compute_factorial(n)
    print(result)