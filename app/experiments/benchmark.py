import time
import csv

from app.crypto.search import SearchableEncryption
from app.db.secure_query import SecureQueryEngine
from app.utils.constants import SEARCH_KEY
from app.experiments.dataset_generator import generate_dataset
from app.db import shard1

OUTPUT_FILE = "benchmark_results.csv"


def run_benchmark():

    se = SearchableEncryption(SEARCH_KEY)
    engine = SecureQueryEngine()

    dataset_sizes = [1000, 5000, 10000]

    keywords = ["salary", "bonus"]
    trapdoors = se.generate_and_trapdoor(keywords)

    results_data = []

    for size in dataset_sizes:
        print(f"\nRunning benchmark for {size} records...")

        # Load dataset
        dataset = generate_dataset(size)
        shard1.load_dataset(dataset)

        # Measure query time
        start = time.time()

        results, _ = engine.secure_read(
            trapdoors=trapdoors,
            user_role="admin",
            user_identifier="sarbasish"
        )

        end = time.time()

        query_time = round(end - start, 6)

        print(f"Query Time: {query_time} sec")

        results_data.append([size, query_time])

    # Save to CSV
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["dataset_size", "query_time"])

        for row in results_data:
            writer.writerow(row)

    print("\nBenchmark saved to benchmark_results.csv")