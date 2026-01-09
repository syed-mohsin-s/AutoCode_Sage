from utils import compute_mean
def login(username, password):
    # TODO: Fix this later
    # Vulnerability: Hardcoded secret and SQL Injection
    secret_key = "12345-SUPER-SECRET" 
    query = "SELECT * FROM users WHERE user = " + username
    execute(query)
def main():
    data = [1, 2, 3, 4, 5]
    print("Average:", compute_mean(data))

if __name__ == "__main__":
    main()
