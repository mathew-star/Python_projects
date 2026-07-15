# Cache Proxy

A small SDK-style caching HTTP proxy built with FastAPI, httpx, Click, and a
from-scratch LRU cache.

## What It Teaches

- async request forwarding with `httpx.AsyncClient`
- FastAPI lifespan context managers
- CLI design with `click`
- LRU cache internals with hashmap + doubly linked list
- stable cache key construction
- package entry points with `uv`

## Run The CLI

From the repository root:

```bash
uv sync
uv run cache-proxy --help
```

Start the proxy:

```bash
uv run cache-proxy run --port 8000 --origin http://localhost:9000
```

Useful options:

```bash
uv run cache-proxy run \
  --port 8000 \
  --origin http://localhost:9000 \
  --cache-capacity 128 \
  --cache-method GET \
  --cache-method HEAD \
  --timeout 30
```

Check cache stats:

```bash
uv run cache-proxy stats --port 8000
```

Clear the cache:

```bash
uv run cache-proxy clear-cache --port 8000
```

## Real Manual Test With FastAPI

Terminal 1: start the sample origin server.

```bash
uv run uvicorn cache_proxy.examples.sample_origin:app --port 9000 --reload
```

Terminal 2: start the cache proxy.

```bash
uv run cache-proxy run --port 8000 --origin http://localhost:9000
```

Terminal 3: call the proxy.

```bash
curl -i http://localhost:8000/time
curl -i http://localhost:8000/time
```

The first response should include:

```text
X-Cache: MISS
```

The second response should include:

```text
X-Cache: HIT
```

The JSON body should stay the same on the cache hit because it came from the
proxy cache instead of the origin server.

Check stats:

```bash
uv run cache-proxy stats --port 8000
```

Expected shape:

```text
size=1
capacity=128
hits=1
misses=1
```

## SDK Usage

You can also create the ASGI app directly:

```python
from cache_proxy import ProxyConfig, create_app

app = create_app(
    ProxyConfig(
        origin="http://localhost:9000",
        cache_capacity=256,
    )
)
```

## Current Cache Policy

By default, only `GET` and `HEAD` responses are cached. This is intentional:
`POST`, `PUT`, `PATCH`, and `DELETE` can have side effects, so caching them by
default would be unsafe.

You can opt into other methods from the CLI:

```bash
uv run cache-proxy run \
  --port 8000 \
  --origin http://localhost:9000 \
  --cache-method GET \
  --cache-method POST
```
