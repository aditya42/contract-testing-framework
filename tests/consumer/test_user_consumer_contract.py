"""Consumer-driven contracts for the UserClient."""

import pytest
from pact import Pact, match

from contract_framework.consumer.client import UserClient, UserNotFoundError


@pytest.mark.consumer_contract
def test_get_existing_user_contract(user_pact: Pact) -> None:
    expected_body = {
        "id": match.int(123),
        "name": match.str("Alice"),
        "email": match.regex("alice@example.com", regex=r"^[^@]+@[^@]+\.[^@]+$"),
        "created_on": match.str("2026-01-15T10:30:00+00:00"),
    }

    (
        user_pact.upon_receiving("a request for an existing user")
        .given("user exists", id=123, name="Alice", email="alice@example.com")
        .with_request("GET", "/users/123")
        .will_respond_with(200)
        .with_body(expected_body, content_type="application/json")
    )

    with user_pact.serve() as server:
        user = UserClient(str(server.url)).get_user(123)

    assert user.id == 123
    assert user.name == "Alice"
    assert user.email == "alice@example.com"


@pytest.mark.consumer_contract
def test_get_missing_user_contract(user_pact: Pact) -> None:
    (
        user_pact.upon_receiving("a request for a missing user")
        .given("user does not exist", id=999)
        .with_request("GET", "/users/999")
        .will_respond_with(404)
        .with_body({"detail": "User not found"}, content_type="application/json")
    )

    with user_pact.serve() as server:
        client = UserClient(str(server.url))
        with pytest.raises(UserNotFoundError, match="User 999 was not found"):
            client.get_user(999)


@pytest.mark.consumer_contract
def test_create_user_contract(user_pact: Pact) -> None:
    request_body = {"name": "Bob", "email": "bob@example.com"}
    response_body = {
        "id": match.int(456),
        "name": "Bob",
        "email": "bob@example.com",
        "created_on": match.str("2026-01-15T10:30:00+00:00"),
    }

    (
        user_pact.upon_receiving("a request to create a user")
        .given("provider accepts user creation")
        .with_request("POST", "/users")
        .with_body(request_body, content_type="application/json")
        .will_respond_with(201)
        .with_body(response_body, content_type="application/json")
    )

    with user_pact.serve() as server:
        user = UserClient(str(server.url)).create_user("Bob", "bob@example.com")

    assert user.id == 456
    assert user.name == "Bob"
    assert user.email == "bob@example.com"
