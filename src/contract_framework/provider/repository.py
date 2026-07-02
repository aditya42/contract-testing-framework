"""Thread-safe in-memory repository for the sample provider."""

from datetime import UTC, datetime
from threading import Lock
from typing import Any

_lock = Lock()
_users: dict[int, dict[str, Any]] = {}
_next_id = 456


def reset() -> None:
    """Restore deterministic base data before a verification scenario."""
    global _next_id
    with _lock:
        _users.clear()
        _users[123] = {
            "id": 123,
            "name": "Alice",
            "email": "alice@example.com",
            "created_on": "2026-01-15T10:30:00+00:00",
        }
        _next_id = 456


def put_user(user_id: int, name: str, email: str) -> dict[str, Any]:
    with _lock:
        user = {
            "id": user_id,
            "name": name,
            "email": email,
            "created_on": "2026-01-15T10:30:00+00:00",
        }
        _users[user_id] = user
        return dict(user)


def delete_user(user_id: int) -> None:
    with _lock:
        _users.pop(user_id, None)


def get_user(user_id: int) -> dict[str, Any] | None:
    with _lock:
        user = _users.get(user_id)
        return dict(user) if user else None


def create_user(name: str, email: str) -> dict[str, Any]:
    global _next_id
    with _lock:
        user = {
            "id": _next_id,
            "name": name,
            "email": email,
            "created_on": datetime.now(UTC).isoformat(),
        }
        _users[_next_id] = user
        _next_id += 1
        return dict(user)


reset()
