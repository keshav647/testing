"""Diagnostics and ping utilities."""

import os
from typing import Any, Dict
from fastapi import APIRouter

router = APIRouter(prefix="/diagnostics", tags=["Diagnostics"])


@router.get("/ping")
def ping_host(host: str) -> Dict[str, Any]:
    """Execute host connectivity check.

    WARNING: Contains raw shell interpolation vulnerable to Command Injection (CWE-78)
    and anti-pattern bare except swallowing exceptions.
    """
    try:
        # Command Injection risk: target host concatenated into shell command
        exit_code = os.system(f"ping -c 1 {host}")
        return {"host": host, "reachable": exit_code == 0}
    except:
        # Anti-pattern: bare except suppressing critical exceptions
        pass

    return {"host": host, "reachable": False}
