from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI


app = FastAPI(title="Sample Origin Server")


@app.get("/time")
async def time() -> dict[str, str]:
    return {
        "now": datetime.now(timezone.utc).isoformat(),
        "request_id": str(uuid4()),
    }


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> dict[str, int | str]:
    return {
        "user_id": user_id,
        "name": f"user-{user_id}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/echo")
async def echo(payload: dict[str, object]) -> dict[str, object]:
    return {
        "payload": payload,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
