"""Fixtures for starting the real provider during Pact verification."""

import socket
import threading
import time
from collections.abc import Generator

import pytest
import requests
import uvicorn

from contract_framework.provider.app import app


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.fixture(scope="session")
def provider_url() -> Generator[str, None, None]:
    port = _free_port()
    url = f"http://127.0.0.1:{port}"
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            if requests.get(f"{url}/health", timeout=0.2).status_code == 200:
                break
        except requests.RequestException:
            time.sleep(0.05)
    else:
        server.should_exit = True
        thread.join(timeout=2)
        raise RuntimeError("Provider failed to start")

    yield url

    server.should_exit = True
    thread.join(timeout=5)
