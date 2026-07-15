from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from cache_proxy.config import ProxyConfig
from cache_proxy.core.cache import CacheEntry, ResponseCache
from cache_proxy.core.cache_key import build_cache_key
from cache_proxy.core.proxy import fetch_from_origin, filter_response_headers


def create_app(config: ProxyConfig) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        http_client = httpx.AsyncClient(
            timeout=config.request_timeout,
            follow_redirects=config.follow_redirects,
        )
        cache = ResponseCache(capacity=config.cache_capacity)

        app.state.config = config
        app.state.http_client = http_client
        app.state.cache = cache

        print(f"Proxy started -> forwarding to {config.origin}")
        yield

        await http_client.aclose()
        print("Proxy shut down cleanly.")

    app = FastAPI(title="Cache Proxy", lifespan=lifespan)

    @app.get("/--cache--/stats", include_in_schema=False)
    async def cache_stats(request: Request) -> JSONResponse:
        cache: ResponseCache = request.app.state.cache
        return JSONResponse(cache.stats())

    @app.delete("/--cache--/clear", include_in_schema=False)
    async def clear_cache(request: Request) -> JSONResponse:
        cache: ResponseCache = request.app.state.cache
        size_before = cache.size()
        cache.clear()
        return JSONResponse({"cleared": True, "entries_removed": size_before})

    @app.api_route(
        "/{path:path}",
        methods=["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )
    async def proxy(request: Request, path: str) -> Response:
        cache: ResponseCache = request.app.state.cache
        client: httpx.AsyncClient = request.app.state.http_client
        active_config: ProxyConfig = request.app.state.config

        body = await request.body()
        target_url = _target_url(active_config.origin, request)
        request_headers = _forward_headers(request)
        can_cache = request.method.upper() in active_config.cache_methods
        cache_key = build_cache_key(
            method=request.method,
            url=target_url,
            body=body,
            headers=request_headers,
        )

        if can_cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return _to_response(cached, cache_status="HIT")

        try:
            origin_response = await fetch_from_origin(
                client=client,
                method=request.method,
                url=target_url,
                headers=request_headers,
                body=body,
            )
        except httpx.RequestError as exc:
            return JSONResponse(
                {
                    "error": "origin_request_failed",
                    "detail": str(exc),
                    "origin": active_config.origin,
                },
                status_code=502,
            )

        if can_cache and _is_cacheable(origin_response):
            cache.set(cache_key, origin_response)

        cache_status = "MISS" if can_cache else "BYPASS"
        return _to_response(origin_response, cache_status=cache_status)

    return app


def _target_url(origin: str, request: Request) -> str:
    target_url = f"{origin}{request.url.path}"
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"
    return target_url


def _forward_headers(request: Request) -> dict[str, str]:
    excluded = {"host", "connection", "content-length"}
    return {
        name: value
        for name, value in request.headers.items()
        if name.lower() not in excluded
    }


def _is_cacheable(entry: CacheEntry) -> bool:
    return 200 <= entry.status_code < 300


def _to_response(entry: CacheEntry, *, cache_status: str) -> Response:
    headers = filter_response_headers(entry.headers)
    headers["X-Cache"] = cache_status
    return Response(
        content=entry.body,
        status_code=entry.status_code,
        headers=headers,
    )


app = create_app(ProxyConfig(origin="http://localhost:9000"))
