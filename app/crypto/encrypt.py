"""
AES-256-GCM encryption module.
All sensitive data is encrypted at application layer
before database insertion.
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.security.key_manager import KeyManager


# Initialize global key manager
key_manager = KeyManager()

'''
KEY_FILE = "aes.key"

# Load or create AES key (persistent)
if not os.path.exists(KEY_FILE):
    AES_KEY = AESGCM.generate_key(bit_length=256)
    with open(KEY_FILE, "wb") as f:
        f.write(AES_KEY)
else:
    with open(KEY_FILE, "rb") as f:
        AES_KEY = f.read()
'''


def encrypt_data(plain_text: str):
    key = key_manager.get_current_key()
    key_version = key_manager.current_version

    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    ciphertext = aesgcm.encrypt(nonce, plain_text.encode(), None)
    return nonce, ciphertext, key_version


'''def decrypt_data(nonce: bytes, ciphertext: bytes) -> str:
    aesgcm = AESGCM(AES_KEY)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()'''


def decrypt_data(nonce: bytes, ciphertext: bytes, key_version: int) -> str:
    key = key_manager.get_key(key_version)

    if key is None:
        raise ValueError("Invalid key version")

    aesgcm = AESGCM(key)

    plaintext = aesgcm.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode()

