# The following Python program crashes at runtime due to an index error.Rewrite the program so that the error is handled safely using exception handling. Instead of crashing, print a meaningful error message. Provide the corrected full code.

names = ["Amit", "Riya", "Suresh"]

try:
    print(names[5])
except IndexError:
    print("Error: Tried to access an index that doesn't exist. Please check the list size.")