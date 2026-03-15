"""Standardized API response helpers."""

from typing import Any


def success_response(data: Any = None, message: str = "Sucesso") -> dict:
    """Return a standardized success envelope."""
    return {"status": "success", "message": message, "data": data}


def error_response(message: str = "Erro", detail: Any = None) -> dict:
    """Return a standardized error envelope."""
    return {"status": "error", "message": message, "detail": detail}
