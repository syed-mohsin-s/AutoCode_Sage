# Intentional error: variable 'result' is used before being defined

def add_numbers(a, b):
    return a + b

print("Sum is:", result)   # <-- ERROR: 'result' is not defined

result = add_numbers(5, 10)
