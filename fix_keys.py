from cryptography.fernet import Fernet
import secrets
import base64

def generate_proper_keys():
    # Generate a proper Fernet key (32 url-safe base64-encoded bytes)
    proper_key = Fernet.generate_key().decode()
    
    # Generate JWT secret
    jwt_secret = secrets.token_urlsafe(32)
    
    print("=" * 60)
    print("PROPER ENCRYPTION KEYS - REPLACE IN YOUR .env FILE:")
    print("=" * 60)
    print(f"ENCRYPTION_KEY={proper_key}")
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print("=" * 60)
    print("\n⚠️  COPY THESE EXACTLY - don't modify them!")
    print("⚠️  Replace the existing keys in your .env file")

if __name__ == "__main__":
    generate_proper_keys()