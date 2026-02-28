import hashlib

from app.db import shard1, shard2, shard3


class ShardRouter:

    def __init__(self):
        self.shards = [shard1, shard2, shard3]

    # --------------------------
    # Deterministic Shard Routing
    # --------------------------
    def route(self, user_identifier: str):
        """
        Routes user to specific shard using hash
        """
        hash_value = int(
            hashlib.sha256(user_identifier.encode()).hexdigest(),
            16
        )

        shard_index = hash_value % len(self.shards)

        return self.shards[shard_index]