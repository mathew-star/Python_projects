from __future__ import annotations
 
import httpx
 
from cache_proxy.core.cache import CacheEntry


HOP_BY_HOP_HEADERS = {
    "connection",
    "content-encoding",
    "content-length",
    "date",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "server",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}


def filter_response_headers(headers: dict[str, str]) -> dict[str, str]:
    return {
        name: value
        for name, value in headers.items()
        if name.lower() not in HOP_BY_HOP_HEADERS
    }




async def fetch_from_origin(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    headers: dict[str, str],
    body: bytes,
) -> CacheEntry:
    """ 
    We will use this func to fire the request to the origin , with the shared client that lives in app.state
    (connection-pooled,created once at startup — never instantiate a new client per request)
    """
    
    

    response = await client.request(
        method=method,
        url=url,
        headers=headers,
        content=body,
    )

    return CacheEntry(
        status_code=response.status_code,
        headers=filter_response_headers(dict(response.headers)),
        body=response.content,
    )
