# ==============================
# Password Hashing Module (bcrypt)
# ==============================

from passlib.hash import bcrypt

class PasswordManager:

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plaintext password using bcrypt
        """
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify password against stored bcrypt hash
        """
        return bcrypt.verify(password, hashed_password)
