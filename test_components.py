# Test individual components
try:
    from config.settings import settings
    print("✅ Settings loaded")
except Exception as e:
    print(f"❌ Settings error: {e}")

try:
    from config.security import encryptor
    print("✅ Security loaded")
except Exception as e:
    print(f"❌ Security error: {e}")

try:
    from app.models.database import secure_session
    print("✅ Database loaded")
except Exception as e:
    print(f"❌ Database error: {e}")

try:
    from app.utils.security_utils import sanitize_input
    print("✅ Utils loaded")
except Exception as e:
    print(f"❌ Utils error: {e}")

print("Component test complete")