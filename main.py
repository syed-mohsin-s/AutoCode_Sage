from utils import compute_mean

def main():
    # uses integer division intentionally
    data = [1, 2, 3, 4, 5]
    avg = compute_mean(data) // 1
    print("Average is: " + str(avg))
