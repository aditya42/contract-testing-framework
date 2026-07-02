"""Consumer contract fixtures."""

import shutil
from collections.abc import Generator
from pathlib import Path

import pytest
from pact import Pact

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACT_DIR = PROJECT_ROOT / "pacts"


@pytest.fixture(scope="session", autouse=True)
def clean_old_contracts() -> Generator[None, None, None]:
    """Prevent stale interactions from leaking into the current build."""
    shutil.rmtree(PACT_DIR, ignore_errors=True)
    PACT_DIR.mkdir(parents=True, exist_ok=True)
    yield


@pytest.fixture
def user_pact() -> Generator[Pact, None, None]:
    """Create one isolated Pact interaction and merge it into the Pact file."""
    pact = Pact("user-consumer", "user-provider").with_specification("V4")
    yield pact
    pact.write_file(PACT_DIR)
