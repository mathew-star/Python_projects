from __future__ import annotations

from collections.abc import Mapping, Sequence
from hashlib import sha256


def build_cache_key(
    *,
    method: str,
    url: str,
    body: bytes = b"",
    headers: Mapping[str, str] | None = None,
    vary_headers: Sequence[str] = (),
) -> str:
    """Build a stable key for requests that should be considered equivalent."""
    parts = [method.upper(), url]

    if body:
        parts.append(f"body_sha256={sha256(body).hexdigest()}")

    if headers and vary_headers:
        lower_headers = {name.lower(): value for name, value in headers.items()}
        for header_name in sorted(vary_headers, key=str.lower):
            value = lower_headers.get(header_name.lower(), "")
            parts.append(f"{header_name.lower()}={value}")

    return "|".join(parts)
