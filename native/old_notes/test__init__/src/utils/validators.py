"""
驗證工具模組 - 提供驗證功能
"""

import re

def is_valid_email(email: str) -> bool:
    """驗證電子郵件格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_valid_phone(phone: str) -> bool:
    """驗證電話號碼格式"""
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone)) 