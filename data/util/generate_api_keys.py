import secrets
import string

def generate_api_key(length=32):
    """Generate a secure API key."""
    characters = string.ascii_letters + string.digits  # Include letters and numbers
    api_key = ''.join(secrets.choice(characters) for _ in range(length))
    return api_key

# Generate and print a secure API key
if __name__ == "__main__":
    api_key = generate_api_key()
    print(f"Generated API Key: {api_key}")