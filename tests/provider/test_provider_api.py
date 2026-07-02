"""Small provider API smoke suite, separate from contract verification."""

import pytest
import requests

from contract_framework.provider import repository


@pytest.fixture(autouse=True)
def reset_repository() -> None:
    repository.reset()


@pytest.mark.provider_api
def test_health_endpoint(provider_url: str) -> None:
    response = requests.get(f"{provider_url}/health", timeout=2)
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


@pytest.mark.provider_api
def test_unknown_user_returns_404(provider_url: str) -> None:
    response = requests.get(f"{provider_url}/users/999", timeout=2)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.provider_api
def test_create_user_returns_201(provider_url: str) -> None:
    response = requests.post(
        f"{provider_url}/users",
        json={"name": "Bob", "email": "bob@example.com"},
        timeout=2,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Bob"
    assert response.json()["email"] == "bob@example.com"
