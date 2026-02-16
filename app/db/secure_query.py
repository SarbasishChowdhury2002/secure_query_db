from typing import List, Dict
from app.auth.rbac import RBAC

# ==============================
# Secure Query Engine with RBAC
# ==============================

class SecureQueryEngine:
    def __init__(self, shards: List[object]):
        self.shards = shards
        self.rbac = RBAC()

    # --------------------------
    # AND-based Secure Search
    # --------------------------
    def and_search(self, trapdoors: List[str], user_role: str) -> List[Dict]:
        """
        Perform multi-keyword AND search with RBAC enforcement
        """

        # 🔐 Authorization check
        if not self.rbac.authorize(user_role, "search"):
            raise PermissionError("Unauthorized search attempt")

        results = []

        for shard in self.shards:
            shard_data = shard.read_all()

            for record in shard_data:
                if all(td in record["tokens"] for td in trapdoors):
                    results.append(record)

        return results
