import time
import tracemalloc
import csv
import pandas as pd
from iter_day1 import CSVIterator  


def benchmark(fn, label):
    tracemalloc.start()
    start = time.perf_counter()

    result = fn()
    print(result)

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "label": label,
        "time": end - start,
        "peak_mem_kb": peak / 1024,
        "result": result,
    }

def custom_lazy_reader():
    count = 0
    for row in CSVIterator("customers-100000.csv"):
        count += 1
    return count


def csv_reader_full():
    with open("customers-100000.csv", "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return len(rows)


def pandas_reader():
    df = pd.read_csv("customers-100000.csv")
    return len(df)



benchmarks = [
    benchmark(custom_lazy_reader, "Custom Lazy CSVIterator"),
    benchmark(csv_reader_full, "Python csv.reader + list()"),
    benchmark(pandas_reader, "pandas.read_csv"),
]

print("\n=== PERFORMANCE RESULTS ===\n")
print(f"{'Method':35} | {'Time (s)':>10} | {'Peak Mem (KB)':>15}")
print("-" * 70)
for b in benchmarks:
    print(f"{b['label']:35} | {b['time']:10.6f} | {b['peak_mem_kb']:15.2f}")
print()

