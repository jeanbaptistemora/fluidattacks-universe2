# Standard library
import asyncio
import os
from typing import (
    AsyncIterator,
    Callable,
    Dict,
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
def test_branch() -> Iterator[str]:
    yield os.environ['CI_COMMIT_REF_NAME']


@pytest.fixture(autouse=True, scope='session')  # type: ignore
def test_group(test_branch: str) -> Iterator[str]:
    mapping: Dict[str, str] = {
        'kamadoatfluid': 'worcester',
        'master': 'tovuz',
    }

    yield mapping.get(test_branch, 'utuado')


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
