import time
import csv

from app.crypto.search import SearchableEncryption
from app.db.secure_query import SecureQueryEngine
from app.utils.constants import SEARCH_KEY
from app.experiments.dataset_generator import generate_dataset
from app.db import shard1, shard2, shard3

OUTPUT_FILE = "shard_benchmark.csv"


def split_dataset(dataset, num_shards):
    return [dataset[i::num_shards] for i in range(num_shards)]


def run_shard_benchmark():

    se = SearchableEncryption(SEARCH_KEY)
    engine = SecureQueryEngine()

    dataset_size = 10000
    REPEAT = 5

    keywords = ["salary", "bonus"]
    trapdoors = se.generate_and_trapdoor(keywords)

    shard_configs = [1, 2, 3]

    results_data = []

    for num_shards in shard_configs:
        print(f"\nRunning with {num_shards} shard(s)")

        dataset = generate_dataset(dataset_size)
        split_data = split_dataset(dataset, num_shards)

        # Load into shards
        if num_shards >= 1:
            shard1.load_dataset(split_data[0])
        if num_shards >= 2:
            shard2.load_dataset(split_data[1])
        if num_shards >= 3:
            shard3.load_dataset(split_data[2])

        total_time = 0

        for _ in range(REPEAT):
            start = time.time()

            results = engine.multi_shard_search(
                trapdoors=trapdoors,
                user_role="admin",
                num_shards=num_shards
            )

            end = time.time()
            total_time += (end - start)

        avg_time = round(total_time / REPEAT, 6)

        print(f"Avg Query Time: {avg_time} sec")

        results_data.append([num_shards, avg_time])

    # Save CSV
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["num_shards", "query_time"])

        for row in results_data:
            writer.writerow(row)

    print("\n✅ Shard benchmark saved to shard_benchmark.csv")