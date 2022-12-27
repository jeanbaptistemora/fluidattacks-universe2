import os
import pytest
from typing import (
    Iterator,
)


@pytest.fixture(scope="session")
def test_group() -> Iterator[str]:
    yield "unittesting"


@pytest.fixture(scope="session")
def test_finding() -> Iterator[str]:
    yield "436992569"


@pytest.fixture(scope="session")
def test_token() -> Iterator[str]:
    yield os.environ["TEST_FORCES_TOKEN"]


@pytest.fixture(scope="session")
def test_endpoint() -> Iterator[str]:
    yield "https://127.0.0.1:8001/api"
