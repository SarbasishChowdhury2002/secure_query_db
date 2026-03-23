import hashlib
import json
from datetime import datetime

BLOCKCHAIN_FILE = "blockchain_log.json"


class Block:
    def __init__(self, query_hash, result_hash, prev_hash):
        self.timestamp = datetime.now().isoformat()
        self.query_hash = query_hash
        self.result_hash = result_hash
        self.prev_hash = prev_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "timestamp": self.timestamp,
            "query_hash": self.query_hash,
            "result_hash": self.result_hash,
            "prev_hash": self.prev_hash
        }, sort_keys=True)

        return hashlib.sha256(block_string.encode()).hexdigest()


class BlockchainLogger:

    def __init__(self):
        self.chain = []

    def get_last_hash(self):
        if not self.chain:
            return "0" * 64  # Genesis previous hash
        return self.chain[-1].hash

    def add_block(self, query_hash, result_hash):
        prev_hash = self.get_last_hash()

        block = Block(query_hash, result_hash, prev_hash)
        self.chain.append(block)

        self.save_block(block)

        return block

    def save_block(self, block):
        data = {
            "timestamp": block.timestamp,
            "query_hash": block.query_hash,
            "result_hash": block.result_hash,
            "prev_hash": block.prev_hash,
            "hash": block.hash
        }

        try:
            with open(BLOCKCHAIN_FILE, "a") as f:
                f.write(json.dumps(data) + "\n")
        except Exception as e:
            print("Blockchain logging error:", e)