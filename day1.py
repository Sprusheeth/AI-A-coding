# function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# generate fibonacci series
def fibonacci_series(n):
    fib_series = [0, 1]
    while len(fib_series) < n:
        next_value = fib_series[-1] + fib_series[-2]
        fib_series.append(next_value)
    return fib_series[:n]