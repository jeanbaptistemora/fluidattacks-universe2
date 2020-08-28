# Standard library
import asyncio
import os
from typing import (
    AsyncIterator,
    Callable,
    Iterator,
)

# Third party libraries
from aioextensions import (
    collect,
    run_decorator,
)
import pytest

# Local libraries
from integrates.graphql import (
    create_session,
    end_session,
)


@pytest.fixture(autouse=True, scope='session')  # type: ignore
def test_config() -> Iterator[Callable[[str], str]]:

    def config(name: str) -> str:
        return f'test/data/config/{name}.yaml'

    yield config


@pytest.fixture(autouse=True, scope='session')  # type: ignore
def test_group() -> Iterator[str]:
    yield 'worcester'


@pytest.fixture(autouse=True, scope='session')  # type: ignore
def test_integrates_api_token() -> Iterator[str]:
    yield os.environ['INTEGRATES_API_TOKEN']


@pytest.fixture(scope='function')  # type: ignore
def test_integrates_session(test_integrates_api_token: str) -> Iterator[None]:
    token = create_session(api_token=test_integrates_api_token)
    try:
        yield
    finally:
        end_session(token)
