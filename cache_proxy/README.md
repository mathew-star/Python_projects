# Cache Proxy -- > Phase 1

A cli-driven cache proxy  build with fastapi and httpx

which the help of cli , now we can run the proxy on a port and give the target origin, to where 
we start forwarding the requests on first hit(miss) , and serving from cache from next one.

### How the pieces connect

main.py   --> CLI (we defined the commands and server startup here)

server.py --> Fastapi + proxy route

proxy.py --> Httpx request to the origin

cache.py --> simple cache with common methods(get / set / clear)

`server.py` owns the lifespan — it creates one shared `httpx.AsyncClient`
(connection pool) and one `DictCache` instance at startup, stores both on
`app.state`, and passes them into every request handler. Nothing is a
bare global except `ORIGIN`, which the CLI sets before `uvicorn.run()`.

## Installation
```bash
git clone <your-repo>
cd cache_proxy
 
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
 
pip install -r requirements.txt
```


## Running it
 
You need two terminals — one for the origin server, one for the proxy.
 
**Terminal 1 — start the origin (fake backend)**
```bash
uvicorn fake_backend:app --port 9000 --reload
```
 
**Terminal 2 — start the proxy**
```bash
python main.py run --port 8000 --origin http://localhost:9000
```
 
Now all traffic through `localhost:8000` is proxied (and cached) to `localhost:9000`.
 
---

## CLI commands
 
### `run` — start the proxy
 
```bash
python main.py run --port PORT --origin URL

#To clear cache >>
python main.py clear-cache --port PORT

```


## What's Next Phase 
Next we will improve the folder structure , add some extra layers.
Main thing is we needed to implement LRU cache from scratch