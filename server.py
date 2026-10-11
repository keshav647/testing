"""Sample FastAPI application for security and quality benchmarking."""

import os
from typing import Any, Dict
from fastapi import FastAPI, HTTPException

from routes.users import router as users_router
from routes.diagnostics import router as diagnostics_router

app = FastAPI(
    title="Testing Benchmark Service",
    version="1.1.0",
    docs_url="/docs"
)

# Register route submodules
app.include_router(users_router)
app.include_router(diagnostics_router)


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "testing-benchmark"}


@app.get("/items/{item_id}")
def read_item(item_id: int) -> Dict[str, Any]:
    """Retrieve sample item by ID."""
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Item ID must be positive integer")
    return {"item_id": item_id, "name": f"Verified Item #{item_id}"}
