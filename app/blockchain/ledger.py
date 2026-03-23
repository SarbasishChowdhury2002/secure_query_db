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
        self.load_chain()


    def load_chain(self):
        try:
            with open(BLOCKCHAIN_FILE, "r") as f:
                for line in f:
                    data = json.loads(line.strip())

                    block = Block(
                        query_hash=data["query_hash"],
                        result_hash=data["result_hash"],
                        prev_hash=data["prev_hash"]
                    )

                    # 🔥 IMPORTANT FIX
                    block.timestamp = data["timestamp"]

                    # recompute hash using stored timestamp
                    recalculated_hash = block.compute_hash()

                    block.hash = data["hash"]

                    # store both for verification
                    block.recalculated_hash = recalculated_hash

                    self.chain.append(block)

        except FileNotFoundError:
            pass

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


    def verify_chain(self):
        for i in range(len(self.chain)):

            current = self.chain[i]

            # 🔥 Check hash integrity
            if current.hash != current.compute_hash():
                return False

            # 🔥 Check linking (skip genesis)
            if i > 0:
                previous = self.chain[i - 1]

                if current.prev_hash != previous.hash:
                    return False

        return True