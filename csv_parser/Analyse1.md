# We are analyzing the current code #


### Why Custom Lazy CSVIterator is so memory efficient ? ###


- it never store rows

- it only count them

- Each row is discarded immediately

- tracemalloc only tracks Python allocations (not OS file buffers)



### why csv reader explodes memory ###

- list(csv.reader(...)) stores 100,000 rows

- Each row is a list of strings

- Each string is a Python object

- This multiplies memory usage massively




### Why pandas.read_csv is fast but memory-heavy ? ###


- Pandas uses C-optimized parsing

- It builds full column arrays

- It eagerly loads everything into memory

- Speed comes from vectorization, not streaming

**What actually happens inside csv.reader?**

```<python>
self.file = open(self.filepath, 'r', encoding='utf-8', newline='')
self.reader = csv.reader(self.file_iter)
```

- csv.reader operates on a TextIOBase-compatible object

- Internally, it relies on TextIOWrapper buffering

- TextIOWrapper eagerly fills its internal buffer

- That buffer is implemented in C, not Python

- Your FileLineIterator is logically bypassed after the first call

**Why tracemalloc reported only ~55 KB**

- tracemalloc tracks Python heap allocations only

- The TextIOWrapper buffer lives in:

    - C heap

    - libc / stdio buffers

    - OS page cache

- That memory is invisible to tracemalloc