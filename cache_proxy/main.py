import typer
import httpx
import uvicorn

import server
from server import app





cli=typer.Typer(help="Cach proxy cli </> ")


@cli.command()
def run(
    port: int = typer.Option(..., help="Port to run proxy server"),
    origin: str = typer.Option(..., help="Origin server URL"),
):
    """
    Start the caching proxy server
    """
    server.ORIGIN = origin.rstrip("/")

    typer.echo(f"Starting proxy on port {port}")
    typer.echo(f"Forwarding requests to {server.ORIGIN}")

    uvicorn.run(app, host="0.0.0.0", port=port)


@cli.command()
def clear_cache(
    port: int = typer.Option(8000, help="Port the proxy is running on"),
):
    """
    Clear the in-memory cache of a running proxy instance.
 
    The proxy exposes a DELETE /--cache--/clear endpoint for exactly this.
    We can't directly call cache.clear() here because the server runs in a
    separate process — we must talk to it over HTTP.
    """
    url = f"http://localhost:{port}/--cache--/clear"
    typer.echo(f"Sending clear-cache request to {url} ...")
    try:
        response = httpx.delete(url, timeout=5.0)
        data = response.json()
        typer.echo(
            typer.style(
                f"Cache cleared — {data['entries_removed']} entries removed.",
                fg=typer.colors.GREEN,
            )
        )
    except httpx.ConnectError:
        typer.echo(
            typer.style(
                f"✗ Could not connect to proxy on port {port}. Is it running?",
                fg=typer.colors.RED,
            ),
            err=True,
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    cli()
