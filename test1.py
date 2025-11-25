# Intentional error: variable 'result' is used before being defined ,

def add_numbers(a, b):
    return a + b

print("Sum is the:", result)   # <-- ERROR: 'result' is not defined

result = add_numbers(35, 45)
