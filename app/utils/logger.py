import json
import time
from datetime import datetime

import csv
import os


LOG_FILE = "query_logs.json"


CSV_FILE = "query_logs.csv"

def log_query_csv(user, role, keywords, shard, query_time):

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header only once
        if not file_exists:
            writer.writerow([
                "timestamp",
                "user",
                "role",
                "keyword_count",
                "shard",
                "query_time"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            user,
            role,
            len(keywords),
            shard,
            query_time
        ])


def log_query(user, role, keywords, shard, query_time):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "role": role,
        "keywords": keywords,
        "keyword_count": len(keywords),
        "shard": shard,
        "query_time": query_time
    }

    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print("Logging error:", e)