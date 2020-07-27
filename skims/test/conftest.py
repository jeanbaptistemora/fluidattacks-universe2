# Standard library
import asyncio
import os
from typing import (
    AsyncIterator,
    Iterator,
)

# Third party libraries
import pytest

# Local libraries
from integrates.graphql import (
    create_session,
)
from utils.model import (
    FindingEnum,
)


@pytest.fixture(scope='session')  # type: ignore
def test_group() -> Iterator[str]:
    yield 'worcester'


@pytest.fixture(scope='session')  # type: ignore
def test_integrates_api_token() -> Iterator[str]:
    yield os.environ['INTEGRATES_API_TOKEN']


@pytest.fixture(scope='function')  # type: ignore
def test_integrates_session(test_integrates_api_token: str) -> Iterator[None]:
    create_session(api_token=test_integrates_api_token)
    yield
