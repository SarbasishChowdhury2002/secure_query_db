from collections import defaultdict

class AccessPatternTracker:

    def __init__(self):
        # keyword → count
        self.pattern_count = defaultdict(int)

    def record_access(self, keywords):
        key = tuple(sorted(keywords))
        self.pattern_count[key] += 1

    def print_patterns(self):
        print("\n📊 Access Pattern Leakage:")

        for k, v in self.pattern_count.items():
            print(f"Keywords {list(k)} → Accessed {v} times")