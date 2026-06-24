import hashlib
import time
from typing import List, Dict, Tuple

from app.config import get_settings
from app.crypto.search import SearchableEncryption
from app.db.secure_query import SecureQueryEngine
from app.blockchain.ledger import BlockchainLogger
from app.utils.logger import log_query, log_query_csv
from app.utils.access_pattern import AccessPatternTracker

settings = get_settings()


class QueryService:

    def __init__(self, blockchain: BlockchainLogger):
        self.se = SearchableEncryption(settings.SEARCH_KEY.encode())
        self.engine = SecureQueryEngine()
        self.blockchain = blockchain
        self.tracker = AccessPatternTracker()

    # --------------------------
    # Core query execution
    # --------------------------
    def run_query(
        self,
        user_identifier: str,
        user_role: str,
        keywords: List[str]
    ) -> Dict:
        """
        Full pipeline: trapdoor → search → decrypt → log → blockchain
        Returns a result dict the UI can directly render.
        """

        if not keywords:
            raise ValueError("At least one keyword is required")

        if not user_identifier.strip():
            raise ValueError("User identifier cannot be empty")

        # Step 1: Generate trapdoors
        trapdoors = self.se.generate_and_trapdoor(keywords)

        # Step 2: Execute secure query
        start = time.time()

        results, shard_index = self.engine.secure_read(
            trapdoors=trapdoors,
            user_role=user_role,
            user_identifier=user_identifier
        )

        query_time = round(time.time() - start, 6)

        # Step 3: Log the query
        shard_name = f"shard{shard_index + 1}"

        log_query(
            user=user_identifier,
            role=user_role,
            keywords=keywords,
            shard=shard_name,
            query_time=query_time
        )

        log_query_csv(
            user=user_identifier,
            role=user_role,
            keywords=keywords,
            shard=shard_name,
            query_time=query_time
        )

        # Step 4: Track access patterns
        self.tracker.record_access(keywords)

        # Step 5: Blockchain logging
        query_hash = hashlib.sha256(
            f"{user_identifier}:{keywords}".encode()
        ).hexdigest()

        result_hash = hashlib.sha256(
            str(results).encode()
        ).hexdigest()

        block = self.blockchain.add_block(query_hash, result_hash)

        # Step 6: Return everything the UI needs
        return {
            "results": results,
            "shard_index": shard_index,
            "shard_name": shard_name,
            "query_time": query_time,
            "trapdoors": dict(zip(keywords, trapdoors)),
            "block_hash": block.hash,
            "prev_hash": block.prev_hash,
            "keyword_count": len(keywords),
            "result_count": len(results)
        }

    # --------------------------
    # Access pattern summary
    # --------------------------
    def get_access_patterns(self) -> Dict:
        return dict(self.tracker.pattern_count)