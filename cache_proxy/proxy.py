from __future__ import annotations
 
import httpx
 
from cache import CacheEntry




async def fetch_from_origin(client:httpx.AsyncClient,
                            method:str,
                            url:str,
                            headers:dict,
                            body:bytes)->CacheEntry:
    """ 
    We will use this func to fire the request to the origin , with the shared client that lives in app.state
    (connection-pooled,created once at startup — never instantiate a new client per request)
    """
    
    

    response= await client.request( 
            method=method,
            url=url,
            headers=headers,
            content=body,   
        )

    return CacheEntry(
            status_code=response.status_code,
            headers=dict(response.headers),
            body= response.content
        )
