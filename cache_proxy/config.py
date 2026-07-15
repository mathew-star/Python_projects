from __future__ import annotations

from dataclasses import dataclass, field


DEFAULT_CACHE_METHODS = frozenset({"GET", "HEAD"})


@dataclass(frozen=True, slots=True)
class ProxyConfig:
    origin: str
    cache_capacity: int = 128
    cache_methods: frozenset[str] = field(default=DEFAULT_CACHE_METHODS)
    request_timeout: float = 30.0
    follow_redirects: bool = True

    def __post_init__(self) -> None:
        origin = self.origin.rstrip("/")
        if not origin:
            raise ValueError("origin must not be empty")

        if self.cache_capacity <= 0:
            raise ValueError("cache_capacity must be greater than 0")

        if self.request_timeout <= 0:
            raise ValueError("request_timeout must be greater than 0")

        normalized_methods = frozenset(method.upper() for method in self.cache_methods)
        object.__setattr__(self, "origin", origin)
        object.__setattr__(self, "cache_methods", normalized_methods)
