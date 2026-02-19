**Custom Lazy CSV Reader --- Performance Benchmark**
==================================================

This project explores how to build a **lazy, memory-efficient CSV reader** in Python using a custom iterator, and compares its performance against two widely used approaches:

1.  Python's built-in `csv.reader` with full file loading

2.  `pandas.read_csv`

The goal is to understand **how iteration, memory usage, and file size affect performance**, and to demonstrate how a carefully designed lazy iterator can scale to large datasets without consuming excessive memory.

**What We Built**
=================

**1\. FileLineIterator**
--------------------------

A custom iterator that reads a file **line-by-line** using the file object's `.readline()` method.

-   Opens the file lazily

-   Reads one line at a time

-   Closes automatically when iteration ends

This gives explicit control over the lifecycle of file I/O.

* * * * *

 **2\. CSVIterator**
---------------------

A wrapper around Python's `csv.reader` that takes **our own file iterator** instead of a file object.

This lets us:

-   Stream CSV files **one row at a time**

-   Maintain extremely low memory usage

-   Build pipelines (transform → validate → process → export)





Traditional CSV reading patterns either:

 Load the entire file into memory

rows = list(csv.reader(f))

Huge memory cost for large files.

Or use pandas, which is fast but memory-heavy

pd.read_csv("sample.csv")

 We wanted a reader that:

Uses constant memory, even for 10GB files

Streams data efficiently

Provides full control over the iteration pipeline

Behaves predictably for ETL, data processing, and production workloads



*Benchmark Results of different size files*


 ➜  csv_parser : python analyze.py

101

101

100

=== PERFORMANCE RESULTS ===

Method                              |   Time (s) |   Peak Mem (KB)

----------------------------------------------------------------------

Custom Lazy CSVIterator             |   0.000633 |           46.86

Python csv.reader + list()          |   0.001111 |          112.14

pandas.read_csv                     |   0.004742 |          317.23

 ➜  csv_parser git:(main) ✗ python analyze.py

100001

100001

100000

=== PERFORMANCE RESULTS ===

Method                              |   Time (s) |   Peak Mem (KB)

----------------------------------------------------------------------

Custom Lazy CSVIterator             |   0.521074 |           55.06

Python csv.reader + list()          |   1.142478 |        82405.15

pandas.read_csv                     |   0.566809 |        53519.46












