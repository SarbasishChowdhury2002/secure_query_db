import os
from typing import Dict

# ==============================
# Key Management System
# ==============================

class KeyManager:

    def __init__(self):
        # Simulated key storage (in real world: HSM or KMS)
        self.keys: Dict[int, bytes] = {}
        self.current_version: int = 1

        # Initialize first key
        self.keys[self.current_version] = self._generate_key()

    # --------------------------
    # Generate new AES key
    # --------------------------
    def _generate_key(self) -> bytes:
        return os.urandom(32)  # 256-bit AES key

    # --------------------------
    # Get current active key
    # --------------------------
    def get_current_key(self) -> bytes:
        return self.keys[self.current_version]

    # --------------------------
    # Get key by version
    # --------------------------
    def get_key(self, version: int) -> bytes:
        return self.keys.get(version)

    # --------------------------
    # Rotate key
    # --------------------------
    def rotate_key(self):
        self.current_version += 1
        self.keys[self.current_version] = self._generate_key()
