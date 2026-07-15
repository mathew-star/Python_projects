from dataclasses import dataclass
from typing import Optional

from cache_proxy.core.lru_cache import LRUCache


@dataclass(frozen=True, slots=True)
class CacheEntry:
    status_code: int
    headers: dict[str, str]
    body: bytes


class ResponseCache:
    def __init__(self, capacity: int = 128) -> None:
        self.store: LRUCache[str, CacheEntry] = LRUCache(capacity=capacity)
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[CacheEntry]:
        entry = self.store.get(key)
        if entry is None:
            self.misses += 1
            return None
        self.hits += 1
        return entry
    
    def set(self, key: str, value: CacheEntry) -> None:
        self.store[key] = value

    def clear(self) -> None:
        self.store.clear()
        self.hits = 0
        self.misses = 0
        
    def size(self) -> int:
        return len(self.store)

    def stats(self) -> dict[str, int]:
        return {
            "size": self.size(),
            "capacity": self.store.capacity,
            "hits": self.hits,
            "misses": self.misses,
        }


DictCache = ResponseCache
