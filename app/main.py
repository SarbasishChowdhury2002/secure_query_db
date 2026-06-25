"""
Secure Query Processing over Encrypted and Sharded Databases
NITK Surathkal — CS850 Database Security

Entry points:
    Streamlit UI  : streamlit run app/ui/application.py
    REST API      : uvicorn app.api.routes:app --reload
    Tests         : pytest tests/test_pipeline.py -v --cov=app
    Benchmarks    : python -m app.main --benchmark
"""

import argparse
from app.experiments.benchmark import run_benchmark
from app.experiments.keyword_benchmark import run_keyword_benchmark
from app.experiments.shard_benchmark import run_shard_benchmark


def run_pipeline():
    """Run a quick end-to-end demo query."""
    import hashlib
    import time
    from app.blockchain.ledger import BlockchainLogger
    from app.services.query_service import QueryService
    from app.experiments.dataset_generator import generate_dataset
    from app.db import shard1

    print("\n===== SECURE QUERY SYSTEM — END-TO-END DEMO =====\n")

    dataset = generate_dataset(1000)
    shard1.load_dataset(dataset)

    blockchain = BlockchainLogger()
    service = QueryService(blockchain)

    result = service.run_query(
        user_identifier="sarbasish",
        user_role="admin",
        keywords=["salary", "bonus"]
    )

    print(f"Shard:        {result['shard_name']}")
    print(f"Query time:   {result['query_time']} sec")
    print(f"Results found:{result['result_count']}")
    print(f"Block hash:   {result['block_hash'][:32]}...")
    print("\n===== DONE =====")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure Query System")
    parser.add_argument("--demo", action="store_true", help="Run end-to-end demo")
    parser.add_argument("--benchmark", action="store_true", help="Run dataset size benchmark")
    parser.add_argument("--keyword-benchmark", action="store_true", help="Run keyword benchmark")
    parser.add_argument("--shard-benchmark", action="store_true", help="Run shard benchmark")
    args = parser.parse_args()

    if args.benchmark:
        run_benchmark()
    elif args.keyword_benchmark:
        run_keyword_benchmark()
    elif args.shard_benchmark:
        run_shard_benchmark()
    else:
        run_pipeline()