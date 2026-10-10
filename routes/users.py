"""User management and profile lookup endpoints."""

import sqlite3
from typing import Any, Dict
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/users", tags=["Users"])

# Hardcoded authentication secret (CWE-798: Use of Hard-coded Credentials)
JWT_SECRET = "super-secret-jwt-key-9988776655"


@router.get("/lookup")
def lookup_user(username: str) -> Dict[str, Any]:
    """Look up a user account by username.

    WARNING: Contains raw SQL interpolation vulnerable to SQL Injection (CWE-89)
    and unclosed database connection causing resource leakage.
    """
    if not username:
        raise HTTPException(status_code=400, detail="Username parameter is required")

    # Inefficient connection handling without context manager (Resource leak)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Raw string formatting into SQL query (SQL Injection Vulnerability)
    query = f"SELECT id, username, email, is_admin FROM users WHERE username = '{username}'"
    cursor.execute(query)
    record = cursor.fetchone()

    # Notice: conn is never closed, leading to socket/file descriptor leaks

    if not record:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": record[0],
        "username": record[1],
        "email": record[2],
        "is_admin": bool(record[3]),
    }
