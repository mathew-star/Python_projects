#!/usr/bin/env python3
"""
Memory-safe CSV benchmark for 5GB+ files.
Runs in small chunks, logs to file, survives crashes.
"""
import time
import gc
import os
import sys
import json
from datetime import datetime
from contextlib import contextmanager

# --- Configuration ---
FILE = "customers_5gb.csv"
CHUNK_SIZE = 100_000  # Process this many rows between memory checks
LOG_FILE = "benchmark_log.jsonl"
RESULTS_FILE = "benchmark_results.json"

# --- Minimal memory measurement (no psutil needed) ---
def get_rss_mb():
    """Get RSS in MB from /proc - works on Linux without psutil."""
    try:
        with open(f'/proc/{os.getpid()}/status') as f:
            for line in f:
                if line.startswith('VmRSS:'):
                    kb = int(line.split()[1])
                    return kb / 1024
    except Exception:
        return 0.0
    return 0.0

# --- Safe logging (no stdout buffer overflow) ---
def log_event(event_type, data):
    """Append-only logging - never crashes VS Code terminal."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        "data": data
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
        f.flush()  # Ensure write even if crash follows

# --- Memory-tracking context manager ---
@contextmanager
def measured_execution(label):
    """Context manager that tracks memory without crashing."""
    gc.collect()
    gc.collect()  # Double collect for thorough cleanup
    
    rss_before = get_rss_mb()
    start_time = time.perf_counter()
    max_rss = rss_before
    
    # Generator that yields progress, collects max RSS
    progress = {
        "rows": 0,
        "max_rss": rss_before,
        "start_time": start_time
    }
    
    def update_progress(rows_processed):
        nonlocal max_rss
        progress["rows"] = rows_processed
        current_rss = get_rss_mb()
        if current_rss > max_rss:
            max_rss = current_rss
        # Log every chunk to track liveness
        if rows_processed % CHUNK_SIZE == 0:
            log_event("progress", {
                "label": label,
                "rows": rows_processed,
                "rss_mb": current_rss,
                "elapsed": time.perf_counter() - start_time
            })
            print(f"  {label}: {rows_processed:,} rows, {current_rss:.1f} MB RSS", 
                  flush=True)  # flush prevents buffer buildup
    
    try:
        yield update_progress
    finally:
        elapsed = time.perf_counter() - start_time
        rss_after = get_rss_mb()
        
        result = {
            "label": label,
            "time_seconds": elapsed,
            "rss_start_mb": rss_before,
            "rss_peak_mb": max_rss,
            "rss_end_mb": rss_after,
            "rss_delta_mb": rss_after - rss_before,
            "rows_processed": progress["rows"]
        }
        log_event("completed", result)

# --- Parsers with chunked processing ---

def custom_lazy_reader():
    """Your CSVIterator - truly streaming."""
    from parser import CSVIterator
    
    with measured_execution("CSVIterator (streaming)") as progress:
        count = 0
        for row in CSVIterator(FILE):
            count += 1
            _ = row[0]  # Minimal work
            if count % CHUNK_SIZE == 0:
                progress(count)
        progress(count)  # Final update
    return count

def csv_reader_streaming():
    """Standard csv - but PROPERLY streaming (no list())."""
    import csv
    
    with measured_execution("csv.reader (streaming)") as progress:
        count = 0
        with open(FILE, "r", encoding="utf-8", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                count += 1
                _ = row[0]
                if count % CHUNK_SIZE == 0:
                    progress(count)
        progress(count)
    return count

def pandas_chunked():
    """Pandas in chunks - the only way it survives 5GB."""
    import pandas as pd
    
    with measured_execution("pandas (chunked)") as progress:
        count = 0
        # Process 100k rows at a time
        chunk_iter = pd.read_csv(FILE, chunksize=CHUNK_SIZE)
        for chunk in chunk_iter:
            count += len(chunk)
            # Explicit cleanup
            del chunk
            gc.collect()
            progress(count)
    return count

def raw_binary_baseline():
    """Absolute minimum - just count lines."""
    with measured_execution("Raw binary (baseline)") as progress:
        count = 0
        with open(FILE, 'rb', buffering=8192) as f:
            for line in f:
                count += 1
                if count % CHUNK_SIZE == 0:
                    progress(count)
        progress(count)
    return count

# --- Main execution with crash recovery ---

def run_single_benchmark(bench_fn, name):
    """Run one benchmark, catch crashes, log results."""
    print(f"\n{'='*50}")
    print(f"Starting: {name}")
    print(f"File size: {os.path.getsize(FILE) / (1024**3):.2f} GB")
    print(f"Press Ctrl+C to skip this benchmark")
    print('='*50)
    
    try:
        result = bench_fn()
        print(f"✓ Completed: {result:,} rows")
        return True
    except KeyboardInterrupt:
        print(f"⊘ Skipped by user")
        log_event("skipped", {"benchmark": name, "reason": "user_interrupt"})
        return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        log_event("failed", {"benchmark": name, "error": str(e)})
        return False

def main():
    # Clear old logs
    for f in [LOG_FILE, RESULTS_FILE]:
        if os.path.exists(f):
            os.remove(f)
    
    # Check file exists
    if not os.path.exists(FILE):
        print(f"ERROR: {FILE} not found")
        sys.exit(1)
    
    benchmarks = [
        (raw_binary_baseline, "Raw binary (baseline)"),
        (custom_lazy_reader, "CSVIterator (streaming)"),
        (csv_reader_streaming, "csv.reader (streaming)"),
        (pandas_chunked, "pandas (chunked)"),
    ]
    
    completed = []
    
    for fn, name in benchmarks:
        if run_single_benchmark(fn, name):
            completed.append(name)
        # Aggressive cleanup between runs
        gc.collect()
        gc.collect()
        time.sleep(1)  # Let OS reclaim memory
    
    # Generate final report from logs
    print("\n" + "="*60)
    print("FINAL REPORT (read from disk, survives crashes)")
    print("="*60)
    
    results = []
    with open(LOG_FILE) as f:
        for line in f:
            entry = json.loads(line)
            if entry["type"] == "completed":
                r = entry["data"]
                results.append(r)
                print(f"\n{r['label']}:")
                print(f"  Time: {r['time_seconds']:.2f}s")
                print(f"  Peak RSS: {r['rss_peak_mb']:.2f} MB")
                print(f"  Delta RSS: {r['rss_delta_mb']:+.2f} MB")
                print(f"  Rows: {r['rows_processed']:,}")
    
    # Save structured results
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed logs: {LOG_FILE}")
    print(f"Results JSON: {RESULTS_FILE}")

if __name__ == "__main__":
    main()