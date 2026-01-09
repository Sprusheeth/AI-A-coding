# Task 1: AI-Generated Logic Without Modularization (Factorial without Functions)
# You are building a small command-line utility for a startup intern onboarding task. The program is simple and must be written quickly without modular design.
# Use GitHub Copilot to generate a Python program that computes a mathematical product-based value (factorial-like logic) directly in the main execution flow, without using any user-defined functions.
import sys
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python day1.py <non-negative integer>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if n < 0:
            raise ValueError
    except ValueError:
        print("Please provide a valid non-negative integer.")
        sys.exit(1)

    product = 1
    for i in range(1, n + 1):
        product *= i

    print(f"The product-based value for {n} is: {product}")