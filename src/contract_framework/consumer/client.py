"""Production-like consumer client exercised by Pact consumer tests."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import requests


@dataclass(frozen=True, slots=True)
class User:
    """User representation required by the consumer application."""

    id: int
    name: str
    email: str
    created_on: datetime


class UserNotFoundError(LookupError):
    """Raised when the provider returns HTTP 404 for a requested user."""


class UserClient:
    """HTTP client for the user-provider API."""

    def __init__(self, base_url: str, timeout_seconds: float = 5.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def get_user(self, user_id: int) -> User:
        response = requests.get(
            f"{self._base_url}/users/{user_id}",
            timeout=self._timeout_seconds,
        )
        if response.status_code == 404:
            raise UserNotFoundError(f"User {user_id} was not found")
        response.raise_for_status()
        return self._to_user(response.json())

    def create_user(self, name: str, email: str) -> User:
        response = requests.post(
            f"{self._base_url}/users",
            json={"name": name, "email": email},
            timeout=self._timeout_seconds,
        )
        response.raise_for_status()
        return self._to_user(response.json())

    @staticmethod
    def _to_user(payload: dict[str, Any]) -> User:
        return User(
            id=int(payload["id"]),
            name=str(payload["name"]),
            email=str(payload["email"]),
            created_on=datetime.fromisoformat(str(payload["created_on"])),
        )
