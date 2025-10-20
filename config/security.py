from cryptography.fernet import Fernet
import base64
from config.settings import settings

class DataEncryptor:
    def __init__(self):
        # The key should already be proper Fernet format from .env
        self.key = settings.ENCRYPTION_KEY
        # Validate it's the right format
        try:
            # This will raise an error if the key is invalid
            Fernet(self.key.encode())
            self.fernet = Fernet(self.key.encode())
        except Exception as e:
            raise ValueError(f"Invalid encryption key: {e}. Please generate a new key using fix_keys.py")
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data like emails and phone numbers"""
        if not data:
            return ""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not encrypted_data:
            return ""
        return self.fernet.decrypt(encrypted_data.encode()).decode()

# Create global encryptor instance
encryptor = DataEncryptor()