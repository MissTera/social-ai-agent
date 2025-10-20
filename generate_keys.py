from cryptography.fernet import Fernet
import secrets

def generate_security_keys():
    encryption_key = Fernet.generate_key().decode()
    jwt_secret = secrets.token_urlsafe(32)
    
    print("=" * 50)
    print("ADD THESE TO YOUR .env FILE:")
    print("=" * 50)
    print(f"ENCRYPTION_KEY={encryption_key}")
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print("=" * 50)

if __name__ == "__main__":
    generate_security_keys()