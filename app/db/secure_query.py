from typing import List, Dict
from app.auth.rbac import RBAC
from app.crypto.encrypt import decrypt_data

# ==============================
# Secure Query Engine with RBAC + Decryption
# ==============================

class SecureQueryEngine:
    def __init__(self, shards: List[object]):
        self.shards = shards
        self.rbac = RBAC()

    # --------------------------
    # AND-based Secure Search
    # --------------------------
    def and_search(self, trapdoors: List[str], user_role: str) -> List[Dict]:

        # 🔐 Authorization check for search
        if not self.rbac.authorize(user_role, "search"):
            raise PermissionError("Unauthorized search attempt")

        results = []

        for shard in self.shards:
            shard_data = shard.read_all()

            for record in shard_data:
                if all(td in record["tokens"] for td in trapdoors):
                    results.append(record)

        return results

    # --------------------------
    # Secure Read with Decrypt
    # --------------------------
    def secure_read(self, trapdoors: List[str], user_role: str) -> List[Dict]:

        encrypted_results = self.and_search(trapdoors, user_role)

        # 🔐 Check decrypt permission
        if not self.rbac.authorize(user_role, "decrypt"):
            # Return ciphertext only
            return encrypted_results

        # If authorized → decrypt
        decrypted_results = []

        for record in encrypted_results:
            decrypted_record = record.copy()
            decrypted_record["plaintext"] = decrypt_data(
                record["nonce"],
                record["ciphertext"]
            )
            decrypted_results.append(decrypted_record)

        return decrypted_results
