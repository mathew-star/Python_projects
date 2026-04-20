from __future__ import annotations
 
from contextlib import asynccontextmanager
from typing import AsyncIterator
 
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
 
from cache import DictCache, CacheEntry
from proxy import fetch_from_origin




ORIGIN: str = ""




@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Everything before 'yield' runs on startup.
    Everything after  'yield' runs on shutdown.
 
    app.state is FastAPI's built-in way to share objects across requests
    without module-level globals that race under concurrency.
    """
    http_client = httpx.AsyncClient(
        timeout=30.0,
        follow_redirects=True,
    )
    cache = DictCache()
 
    app.state.http_client = http_client
    app.state.cache = cache
 
    print(f"Proxy started  →  forwarding to '{ORIGIN}'")
    yield  #  server is running here
 
    await http_client.aclose()
    print("Proxy shut down cleanly.")
 
 
    
    
    

app = FastAPI(title="Cache Proxy", lifespan=lifespan)



@app.delete("/--cache--/clear", include_in_schema=False)
async def clear_cache(request: Request) -> JSONResponse:
    """
    Internal endpoint so the CLI can clear the in-process cache over HTTP.
    Prefixed with '--' so it never collides with a real upstream path.
    """
    cache: DictCache = request.app.state.cache
    size_before = cache.size()
    cache.clear()
    return JSONResponse({"cleared": True, "entries_removed": size_before})




@app.api_route("/{path:path}",methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request:Request,path:str):
    
    cache: DictCache = request.app.state.cache
    client: httpx.AsyncClient = request.app.state.http_client
    
    
    raw_path = request.url.path      
    target_url = f"{ORIGIN}{raw_path}"
    
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"

    cache_key= f"{request.method}:{target_url}"

    cached: CacheEntry | None = cache.get(cache_key)

    if cached:
        return Response(
            content=cached.body,
            status_code= cached.status_code,
            headers = {**cached.headers,"X-Cache":"HIT"}

        )
    
    body=await request.body()
    response = await fetch_from_origin(
        client=client,
        method=request.method,
        url=target_url,
        headers=dict(request.headers),
        body=body,

    )

    
    if 200 <= response.status_code < 300:
        cache.set(cache_key, response)
    

    return Response(
        content=response.body,
        status_code=response.status_code,
        headers={**response.headers, "X-Cache": "MISS"},
    )






