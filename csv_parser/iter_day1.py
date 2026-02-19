"""
we are building a csv reader, so usually we read Read csv like this >>
import csv

with open("sample.csv", "r", encoding="utf-8") as f:
    rows = list(csv.reader(f))   # <-- loads ALL rows into RAM

But in this program we are building a custom csv parser , which reads without loading the whole file into the memory.
we here use iterator to lazily read the file line by line..
"""


import csv
import io
import codecs

class CSVIterator:
    """
    Lazily iterate over a CSV file without loading it wholly into memory.
        Internally we open the file in *binary* mode and yield one raw line
        at a time; csv.reader then parses that line only.
    """
    def __init__(self, filepath, **fmtparams):  
        print(file)
        self.filepath = filepath
        self.fmtparams = fmtparams          # delimiter, quotechar, …
        self._file = None
        self._decoder = None
        self._reader = None
        
    def __enter__(self):
        self._file = open(self.filepath, 'rb')        # raw bytes
        self._decoder = codecs.getreader('utf-8')(self._file)
        self._reader = csv.reader(self._line_generator(), **self.fmtparams)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._reader)
    
    # ---------- internal line generator ----------
    def _line_generator(self):
        """Yield exactly one line per iteration (no extra buffering)."""
        for line in self._decoder:
            yield line




def CSVIteratorOldAPI(filepath, **fmtparams):
    """
    Old-style iterator (no context manager) – kept only so the benchmark
    can switch between the two implementations without changing call-sites.
    """
    class _Old:
        def __init__(self, path, params):
            
            self._iter = CSVIterator(path, **params)
            self._iter.__enter__()

        def __iter__(self):
            return self

        def __next__(self):
            try:
                return next(self._iter)
            except StopIteration:
                self._iter.__exit__(None, None, None)
                raise

    return _Old(filepath, fmtparams)




