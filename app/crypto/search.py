import hmac
import hashlib
from typing import List

# ==============================
# Searchable Encryption Module
# ==============================

class SearchableEncryption:
    def __init__(self, search_key: bytes):
        self.search_key = search_key

    # --------------------------
    # Keyword Token Generation
    # --------------------------
    def generate_token(self, keyword: str) -> str:
        """
        Generates encrypted keyword token for storage
        """
        return hmac.new(
            self.search_key,
            keyword.encode(),
            hashlib.sha256
        ).hexdigest()

    # --------------------------
    # Trapdoor Generation
    # --------------------------
    def generate_trapdoor(self, keyword: str) -> str:
        """
        Generates trapdoor for secure search query
        """
        return hmac.new(
            self.search_key,
            keyword.encode(),
            hashlib.sha256
        ).hexdigest()

    # --------------------------
    # Multi-keyword AND Trapdoor
    # --------------------------
    def generate_and_trapdoor(self, keywords: List[str]) -> List[str]:
        """
        Generates trapdoors for multi-keyword AND search
        """
        return [self.generate_trapdoor(k) for k in keywords]
