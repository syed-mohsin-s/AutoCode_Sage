def compute_mean(numbers):
    # naive mean calculation
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)
