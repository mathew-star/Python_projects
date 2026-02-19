import io
import csv
from typing import List, Optional

class CSVIterator:
    """
    Streaming CSV iterator with O(1) memory and near-native speed.
    
    Strategy:
    - Read raw bytes line by line (no TextIOWrapper buffer)
    - Fast path: no quotes -> bytes.split(b',') [C-speed]
    - Slow path: has quotes -> csv.reader on single decoded line
    """
    
    def __init__(self, filepath: str, **fmtparams):
        self.filepath = filepath
        self.fmtparams = fmtparams
        self._file: Optional[io.BufferedReader] = None
        self._encoding = fmtparams.pop('encoding', 'utf-8')
        # Pre-encode delimiter for fast path
        self._delimiter = fmtparams.get('delimiter', ',').encode(self._encoding)
        
    def __iter__(self):
        # Small buffer for syscalls, but we control line-by-line
        self._file = open(self.filepath, 'rb', buffering=8192)
        return self
    
    def _parse_simple(self, raw: bytes) -> List[str]:
        """Fast path: C-level bytes split + decode per field."""
        # bytes.split is implemented in C, very fast
        fields = raw.split(self._delimiter)
        # Decode each field (small, cache-friendly)
        return [f.decode(self._encoding) for f in fields]
    
    def _parse_complex(self, raw: bytes) -> List[str]:
        """Slow path: proper CSV parsing for quoted fields."""
        line = raw.decode(self._encoding)
        # csv.reader on single line - correct but slower
        return next(csv.reader([line], **self.fmtparams))
    
    def __next__(self) -> List[str]:
        raw = self._file.readline()
        if not raw:
            self._file.close()
            self._file = None
            raise StopIteration
        
        # Strip \r\n or \n (handle both Unix and Windows line endings)
        if raw.endswith(b'\n'):
            raw = raw[:-1]
        if raw.endswith(b'\r'):
            raw = raw[:-1]
        
        # Empty line after stripping
        if not raw:
            return []
        
        # Fast path: no quotes, no escapes -> simple split
        # Check for quotechar (default ")
        if b'"' not in raw:
            return self._parse_simple(raw)
        else:
            return self._parse_complex(raw)
    
    def __del__(self):
        if self._file and not self._file.closed:
            self._file.close()