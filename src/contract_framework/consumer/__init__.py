"""Consumer-side API client code."""

from contract_framework.consumer.client import User, UserClient, UserNotFoundError

__all__ = ["User", "UserClient", "UserNotFoundError"]
