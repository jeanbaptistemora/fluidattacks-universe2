import os
import pytest
from typing import (
    Iterator,
)


@pytest.fixture(scope="session")
def test_group() -> Iterator[str]:
    yield "herrin"


@pytest.fixture(scope="session")
def test_finding() -> Iterator[str]:
    yield "940350540"


@pytest.fixture(scope="session")
def test_token() -> Iterator[str]:
    yield os.environ["INTEGRATES_FORCES_API_TOKEN"]


@pytest.fixture(scope="session")
def test_endpoint() -> Iterator[str]:
    yield "https://127.0.0.1:8001/api"
