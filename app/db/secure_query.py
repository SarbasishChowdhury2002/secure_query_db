'''from typing import List, Dict
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
                record["ciphertext"],
                record["key_version"]
            )
            decrypted_results.append(decrypted_record)

        return decrypted_results
'''



from typing import List, Dict
from app.auth.rbac import RBAC
from app.crypto.encrypt import decrypt_data
from app.coordinator.query_router import ShardRouter
from concurrent.futures import ThreadPoolExecutor

class SecureQueryEngine:

    def __init__(self):
        self.rbac = RBAC()
        self.router = ShardRouter()

    # --------------------------
    # AND-based Secure Search
    # --------------------------
    def and_search(
        self,
        trapdoors: List[str],
        user_role: str,
        user_identifier: str
    ) -> List[Dict]:

        # 🔐 Check search permission
        if not self.rbac.authorize(user_role, "search"):
            raise PermissionError("Unauthorized search attempt")

        # 🔄 Route to correct shard
        shard, shard_index = self.router.route(user_identifier)

        results = []
        shard_data = shard.read_all()

        for record in shard_data:
            if all(td in record["tokens"] for td in trapdoors):
                results.append(record)

        return results, shard_index

    # --------------------------
    # Secure Read with Decrypt
    # --------------------------
    def secure_read(
        self,
        trapdoors: List[str],
        user_role: str,
        user_identifier: str
    ) -> List[Dict]:

        encrypted_results, shard_index = self.and_search(
            trapdoors,
            user_role,
            user_identifier
        )

        # 🔐 If no decrypt permission → return ciphertext only
        if not self.rbac.authorize(user_role, "decrypt"):
            return encrypted_results, shard_index

        # 👑 Admin or decrypt-capable role
        decrypted_results = []

        for record in encrypted_results:
            decrypted_record = record.copy()

            decrypted_record["plaintext"] = decrypt_data(
                record["nonce"],
                record["ciphertext"],
                record["key_version"]
            )

            decrypted_results.append(decrypted_record)

        return decrypted_results, shard_index
    

    def multi_shard_search(self, trapdoors, user_role, num_shards):

        if not self.rbac.authorize(user_role, "search"):
            raise PermissionError("Unauthorized search")

        selected_shards = self.router.shards[:num_shards]

        def search_shard(shard):
            results = []
            shard_data = shard.read_all()

            for record in shard_data:
                if all(td in record["tokens"] for td in trapdoors):
                    results.append(record)

            return results

        # 🔥 Parallel execution
        all_results = []

        with ThreadPoolExecutor() as executor:
            results_list = executor.map(search_shard, selected_shards)

        for r in results_list:
            all_results.extend(r)

        return all_results