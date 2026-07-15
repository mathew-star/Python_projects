import click
import httpx
import uvicorn

from cache_proxy.config import DEFAULT_CACHE_METHODS, ProxyConfig
from cache_proxy.server import create_app


@click.group(help="Cache proxy CLI.")
def cli() -> None:
    pass


@cli.command()
@click.option(
    "--port",
    required=True,
    type=int,
    help="Port to run proxy server.",
)
@click.option(
    "--origin",
    required=True,
    help="Origin server URL.",
)
@click.option(
    "--cache-capacity",
    default=128,
    show_default=True,
    type=int,
    help="Maximum number of responses stored in the LRU cache.",
)
@click.option(
    "--cache-method",
    "cache_methods",
    multiple=True,
    default=tuple(sorted(DEFAULT_CACHE_METHODS)),
    show_default=True,
    help="HTTP method to cache. Can be passed multiple times.",
)
@click.option(
    "--timeout",
    default=30.0,
    show_default=True,
    type=float,
    help="Origin request timeout in seconds.",
)
def run(
    port: int,
    origin: str,
    cache_capacity: int,
    cache_methods: tuple[str, ...],
    timeout: float,
) -> None:
    """
    Start the caching proxy server.
    """
    config = ProxyConfig(
        origin=origin,
        cache_capacity=cache_capacity,
        cache_methods=frozenset(cache_methods),
        request_timeout=timeout,
    )
    app = create_app(config)

    click.echo(f"Starting proxy on port {port}")
    click.echo(f"Forwarding requests to {config.origin}")
    click.echo(f"Cache capacity: {config.cache_capacity}")
    click.echo(f"Cache methods: {', '.join(sorted(config.cache_methods))}")

    uvicorn.run(app, host="0.0.0.0", port=port)


@cli.command("clear-cache")
@click.option(
    "--port",
    default=8000,
    show_default=True,
    type=int,
    help="Port the proxy is running on.",
)
def clear_cache(
    port: int,
) -> None:
    """
    Clear the in-memory cache of a running proxy instance.
 
    The proxy exposes a DELETE /--cache--/clear endpoint for exactly this.
    We can't directly call cache.clear() here because the server runs in a
    separate process — we must talk to it over HTTP.
    """
    url = f"http://localhost:{port}/--cache--/clear"
    click.echo(f"Sending clear-cache request to {url} ...")
    try:
        response = httpx.delete(url, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        click.echo(
            click.style(
                f"Cache cleared — {data['entries_removed']} entries removed.",
                fg="green",
            )
        )
    except httpx.ConnectError:
        click.echo(
            click.style(
                f"Could not connect to proxy on port {port}. Is it running?",
                fg="red",
            ),
            err=True,
        )
        raise click.ClickException("Proxy is not reachable.") from None
    except httpx.HTTPStatusError as exc:
        raise click.ClickException(
            f"Proxy returned HTTP {exc.response.status_code}."
        ) from exc


@cli.command("stats")
@click.option(
    "--port",
    default=8000,
    show_default=True,
    type=int,
    help="Port the proxy is running on.",
)
def stats(port: int) -> None:
    """Print cache stats from a running proxy instance."""
    url = f"http://localhost:{port}/--cache--/stats"
    try:
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()
    except httpx.ConnectError:
        raise click.ClickException(
            f"Could not connect to proxy on port {port}."
        ) from None
    except httpx.HTTPStatusError as exc:
        raise click.ClickException(
            f"Proxy returned HTTP {exc.response.status_code}."
        ) from exc

    data = response.json()
    click.echo(f"size={data['size']}")
    click.echo(f"capacity={data['capacity']}")
    click.echo(f"hits={data['hits']}")
    click.echo(f"misses={data['misses']}")


if __name__ == "__main__":
    cli()
