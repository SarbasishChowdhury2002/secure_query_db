import time
import csv

from app.crypto.search import SearchableEncryption
from app.db.secure_query import SecureQueryEngine
from app.utils.constants import SEARCH_KEY
from app.experiments.dataset_generator import generate_dataset
from app.db import shard1

OUTPUT_FILE = "keyword_benchmark.csv"


def run_keyword_benchmark():

    # Initialize
    se = SearchableEncryption(SEARCH_KEY)
    engine = SecureQueryEngine()

    dataset_size = 5000   # fixed dataset size for fair comparison
    REPEAT = 5            # number of runs for averaging

    queries = [
        ["salary"],
        ["salary", "bonus"],
        ["salary", "bonus", "tax"]
    ]

    print(f"\nLoading dataset with {dataset_size} records...")
    dataset = generate_dataset(dataset_size)
    shard1.load_dataset(dataset)

    results_data = []

    # Run experiments
    for q in queries:
        print(f"\nRunning query: {q}")

        trapdoors = se.generate_and_trapdoor(q)

        total_time = 0

        for _ in range(REPEAT):
            start = time.time()

            results, _ = engine.secure_read(
                trapdoors=trapdoors,
                user_role="admin",
                user_identifier="sarbasish"
            )

            end = time.time()
            total_time += (end - start)

        avg_time = round(total_time / REPEAT, 6)

        print(f"Average Query Time: {avg_time} sec")

        results_data.append([len(q), avg_time])

    # Save results
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["num_keywords", "query_time"])

        for row in results_data:
            writer.writerow(row)

    print("\n✅ Keyword benchmark saved to keyword_benchmark.csv")