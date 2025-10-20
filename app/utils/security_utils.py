import re
from typing import Any, Dict

def sanitize_input(input_string: str) -> str:
    """
    Basic input sanitization to prevent injection attacks
    """
    if not input_string:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[;\\\'"(){}[\]<>]', '', input_string)
    # Limit length
    sanitized = sanitized[:255]
    
    return sanitized.strip()

def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mask sensitive data for logging
    """
    sensitive_fields = ['password', 'api_key', 'secret', 'token', 'authorization', 'email', 'phone']
    masked_data = data.copy()
    
    for key, value in masked_data.items():
        if any(sensitive in key.lower() for sensitive in sensitive_fields) and value:
            if len(str(value)) > 4:
                masked_data[key] = str(value)[:2] + '***' + str(value)[-2:]
            else:
                masked_data[key] = '***'
    
    return masked_data