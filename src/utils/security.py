import hashlib
import secrets
import re
import os

class Security:
    def __init__(self):
        pass
        
    @staticmethod
    def generate_salt(length: int = 32) -> str:
        """Generate a random salt for password hashing."""
        return os.urandom(length).hex()

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """Hash a password with the given salt using SHA-256."""
        salted = password + salt
        return hashlib.sha256(salted.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, salt: str, hashed_password: str) -> bool:
        """Verify if a password matches its hash."""
        return Security.hash_password(password, salt) == hashed_password
        
    def validate_username(self, username: str) -> bool:
        """Validate username format."""
        # Username must be 3-20 characters long and contain only letters, numbers, and underscores
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))
        
    def validate_password(self, password: str) -> bool:
        """Validate password strength."""
        # Password must be at least 8 characters long and contain:
        # - At least one uppercase letter
        # - At least one lowercase letter
        # - At least one number
        # - At least one special character
        if len(password) < 8:
            return False
            
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        return all([has_upper, has_lower, has_digit, has_special]) 