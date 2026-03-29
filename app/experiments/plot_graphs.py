import csv
import matplotlib.pyplot as plt


# -----------------------------
# GRAPH 1: Dataset Size vs Time
# -----------------------------
def plot_dataset_graph():
    x = []
    y = []

    with open("benchmark_results.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x.append(int(row["dataset_size"]))
            y.append(float(row["query_time"]))

    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title("Dataset Size vs Query Time")
    plt.xlabel("Dataset Size")
    plt.ylabel("Query Time (sec)")
    plt.grid()
    plt.savefig("dataset_vs_time.png")
    plt.show()


# -----------------------------
# GRAPH 2: Keywords vs Time
# -----------------------------
def plot_keyword_graph():
    x = []
    y = []

    with open("keyword_benchmark.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x.append(int(row["num_keywords"]))
            y.append(float(row["query_time"]))

    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title("Number of Keywords vs Query Time")
    plt.xlabel("Number of Keywords")
    plt.ylabel("Query Time (sec)")
    plt.grid()
    plt.savefig("keywords_vs_time.png")
    plt.show()


# -----------------------------
# GRAPH 3: Shards vs Time
# -----------------------------
def plot_shard_graph():
    x = []
    y = []

    with open("shard_benchmark.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x.append(int(row["num_shards"]))
            y.append(float(row["query_time"]))

    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title("Number of Shards vs Query Time")
    plt.xlabel("Number of Shards")
    plt.ylabel("Query Time (sec)")
    plt.grid()
    plt.savefig("shards_vs_time.png")
    plt.show()


# -----------------------------
# MAIN
# -----------------------------
def run_all_plots():
    plot_dataset_graph()
    plot_keyword_graph()
    plot_shard_graph()


if __name__ == "__main__":
    run_all_plots()